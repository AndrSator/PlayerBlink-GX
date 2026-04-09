import os
import sys
import time

from enum import Enum, auto
from threading import Thread, Lock
from pygrabber.dshow_graph import FilterGraph

from PySide6.QtCore import QObject, Signal

from src.log import logger
from src.constants import Constants as Const
from src.preferences import Preferences as Prefs

if not Const.MSMF_HW_TRANSFORMS:
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import cv2

if sys.platform == "win32":
    import win32gui
    import win32process
    from .windowcapture import WindowCapture

__version__ = "1.0.0"


# region Models and Enums
class Device:
    """ Represents an input device (webcam, capture card, etc.) """

    def __init__(self, index, name):
        self._index = index
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def index(self):
        return self._index

    def __str__(self):
        return f"{self._name} ({self._index})"


class Window:
    """ Represents a window to capture (monitor mode/Windows only) """

    def __init__(self, handle, title, pid):
        self._handle = handle
        self._title = title
        self._pid = pid

    @property
    def handle(self):
        return self._handle

    @property
    def title(self):
        return self._title

    @property
    def pid(self):
        return self._pid

    def __str__(self):
        return f"{self._title} ({self._pid})"


class CaptureState(Enum):
    IDLE = auto()
    CAPTURING = auto()
    PAUSED = auto()
    ERROR = auto()
    MINIMIZED = auto()


class CvControl(QObject):
    """ Manages video capture from devices and windows,
    and mediates state transitions """

    # Machine transitions
    _VALID_TRANSITIONS = {
        (CaptureState.IDLE, CaptureState.CAPTURING),
        (CaptureState.CAPTURING, CaptureState.PAUSED),
        (CaptureState.CAPTURING, CaptureState.IDLE),
        (CaptureState.PAUSED, CaptureState.CAPTURING),
        (CaptureState.PAUSED, CaptureState.IDLE),
        (CaptureState.IDLE, CaptureState.ERROR),
        (CaptureState.CAPTURING, CaptureState.ERROR),
        (CaptureState.PAUSED, CaptureState.ERROR),
        (CaptureState.ERROR, CaptureState.IDLE),
        (CaptureState.IDLE, CaptureState.MINIMIZED),
        (CaptureState.CAPTURING, CaptureState.MINIMIZED),
        (CaptureState.PAUSED, CaptureState.MINIMIZED),
        (CaptureState.MINIMIZED, CaptureState.CAPTURING),
        (CaptureState.MINIMIZED, CaptureState.IDLE),
        (CaptureState.MINIMIZED, CaptureState.ERROR)
    }

    _PROP_NAMES = {
        cv2.CAP_PROP_FRAME_WIDTH: "FRAME_WIDTH",
        cv2.CAP_PROP_FRAME_HEIGHT: "FRAME_HEIGHT",
        cv2.CAP_PROP_FPS: "FPS",
        cv2.CAP_PROP_BUFFERSIZE: "BUFFERSIZE",
        cv2.CAP_PROP_FOURCC: "FOURCC",
        cv2.CAP_PROP_BRIGHTNESS: "BRIGHTNESS",
        cv2.CAP_PROP_CONTRAST: "CONTRAST",
        cv2.CAP_PROP_SATURATION: "SATURATION",
        cv2.CAP_PROP_EXPOSURE: "EXPOSURE",
        cv2.CAP_PROP_AUTO_EXPOSURE: "AUTO_EXPOSURE",
        cv2.CAP_PROP_GAIN: "GAIN",
        cv2.CAP_PROP_GAMMA: "GAMMA",
        cv2.CAP_PROP_WB_TEMPERATURE: "WB_TEMPERATURE",
        cv2.CAP_PROP_AUTO_WB: "AUTO_WB",
        cv2.CAP_PROP_AUTOFOCUS: "AUTOFOCUS",
        cv2.CAP_PROP_FOCUS: "FOCUS",
        getattr(cv2, "CAP_PROP_QUALITY", -1): "QUALITY",
        cv2.CAP_PROP_BACKEND: "BACKEND",
        cv2.CAP_PROP_CONVERT_RGB: "CONVERT_RGB",
        cv2.CAP_PROP_MODE: "MODE",
        cv2.CAP_PROP_CODEC_PIXEL_FORMAT: "CODEC_PIXEL_FORMAT",
    }

    # Signals
    capture_started = Signal(bool)
    window_minimized = Signal(bool)

    def __init__(self):
        super().__init__()

        self._graph = FilterGraph()

        self._state = CaptureState.IDLE
        self._capture = None
        self._last_frame = None
        self._lock = Lock()
        self._worker = None
        self._running = False

        # Video capture devices
        self._devices = []
        self._current_device = None

        # Windows (monitor mode)
        self._windows = []
        self._current_window = None
        self._monitor_mode = False
        self._blacklist = None

        self.populate_blacklist()
        self.setup_windows()

        # Debug
        self._fps = 0
        self._frame_count = 0
        self._fps_last = 0

    # region State queries
    def is_capturing(self):
        return self._state == CaptureState.CAPTURING

    def is_paused(self):
        return self._state == CaptureState.PAUSED

    def is_idle(self):
        return self._state == CaptureState.IDLE

    def in_error(self):
        return self._state == CaptureState.ERROR

    def is_minimized(self):
        return self._state == CaptureState.MINIMIZED

    def is_active(self):
        return self._state in (CaptureState.CAPTURING,
                               CaptureState.PAUSED,
                               CaptureState.MINIMIZED)
    # endregion

    # region Devices
    @property
    def current_device(self):
        return self._current_device

    @current_device.setter
    def current_device(self, value):
        if value is not None and not isinstance(value, Device):
            raise TypeError("current_device must be a Device instance or None")

        self._current_device = value

    def setup_devices(self):
        self._devices = [Device(index, name) for index,
                         name in enumerate(self._graph.get_input_devices())]

        if self.current_device is None:
            self.current_device = self._devices[0] if self._devices else None

        logger.debug(
            self._devices and f"[CvControl] Available devices: {[
                str(d) for d in self._devices]}" or "No capture devices found")

    def set_next_device(self):
        self._set_device_by_offset(1)

    def set_prev_device(self):
        self._set_device_by_offset(-1)

    def _set_device_by_offset(self, offset: int):
        if not self._devices or len(self._devices) <= 1:
            return

        curr_index = self.current_device.index
        next_index = (curr_index + offset) % len(self._devices)
        self.set_device(self._devices[next_index])
        logger.debug(f"[CvControl] Device switched to: {self.current_device}")

    def _prop_name(self, prop_id: int) -> str:
        return self._PROP_NAMES.get(prop_id, f"PROP_{int(prop_id)}")

    # endregion

    # region Monitor mode
    @property
    def monitor_mode(self):
        return self._monitor_mode

    @monitor_mode.setter
    def monitor_mode(self, value):
        if not isinstance(value, bool):
            raise TypeError("monitor_mode must be a boolean")

        self._monitor_mode = value

    @property
    def windows(self):
        return self._windows

    @windows.setter
    def windows(self, value):
        if value is None:
            self._windows = None
            return

        if not isinstance(value, list):
            raise TypeError("Windows must be a list of Window instances")

        if not all(isinstance(w, Window) for w in value):
            raise TypeError("All items in windows must be Window instances")

        self._windows = value

    @property
    def current_window(self):
        return self._current_window

    @current_window.setter
    def current_window(self, value):
        if value is not None and not isinstance(value, Window):
            raise TypeError("current_window must be a Window or None")

        self._current_window = value

    def get_windows_titles(self):
        windows_titles = [w.title for w in self.windows]
        logger.debug(f"[CvControl]Available windows: {windows_titles}")
        return windows_titles

    def populate_blacklist(self):
        self._blacklist = []

        try:
            logger.debug(
                f"[CvControl] Loading blacklist from: {Const.BL_FILE}")
            with open(Const.BL_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()

                    if not line or line.startswith("#"):
                        continue

                    try:
                        self._blacklist.append(line)
                    except Exception as e_line:
                        logger.warning(
                            f"[CvControl] Invalid line '{line}': {e_line}")

        except Exception as e_file:
            logger.error(
                f"[CvControl] Error opening/reading blacklist from "
                f"{Const.BL_FILE}: {e_file}")
            self._blacklist = None

        logger.debug(f"[CvControl] Blacklist loaded: {self._blacklist}")

    def setup_windows(self):
        if sys.platform != 'win32':  # Windows only
            self.windows = []
            return

        current_pid = os.getpid()
        windows = []

        def callback(hwnd, _):
            if not win32gui.IsWindowVisible(hwnd):
                return

            title = win32gui.GetWindowText(hwnd)
            if not title:
                return

            if self._blacklist and \
                    any(w.lower() in title.lower() for w in self._blacklist):
                return

            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            # Ignore self windows to avoid capture conflicts
            if pid == current_pid:
                return

            windows.append(Window(hwnd, title, pid))

        win32gui.EnumWindows(callback, None)

        self._windows = windows

        logger.debug(
            self._windows and f"[CvControl] Available windows: {[
                str(w) for w in self._windows]}" or "No windows found")

    def refresh_windows(self):
        self.setup_windows()
        return self.windows

    def toggle_monitor_mode(self):
        if sys.platform != 'win32':  # Windows only
            self.monitor_mode = False
            logger.warning(
                "[CvControl] Monitor mode is only available on Windows.")
            return

        self.monitor_mode = not self.monitor_mode

        return self.monitor_mode

    # endregion

    # region State machines
    @property
    def state(self):
        return self._state

    def start_capture(self):
        self._stop_worker()

        with self._lock:
            if self._state == CaptureState.CAPTURING:
                return

            if self._state == CaptureState.PAUSED:
                self._transition(CaptureState.CAPTURING)
                return

            if self.monitor_mode:
                if self.current_window is None:
                    self._transition(CaptureState.ERROR)
                    self.capture_started.emit(False)
                    return

                target_loop = self._window_capture_loop
            else:
                if self.current_device is None:
                    self._transition(CaptureState.ERROR)
                    self.capture_started.emit(False)
                    return

                target_loop = self._capture_loop

        self._running = True
        self._worker = Thread(target=target_loop, daemon=True)
        self._worker.start()

    def _transition(self, target):
        if self._state == target:
            return

        if (self._state, target) not in self._VALID_TRANSITIONS:
            raise InvalidStateTransition(self._state, target)

        logger.debug(
            f"[CvControl] Transition: "
            f"{self._state.name} -> {target.name}")
        self._state = target

    def _stop_worker(self):
        self._running = False

        if self._worker is not None:
            self._worker.join(timeout=10)
            self._worker = None

        with self._lock:
            if self._capture is not None:
                self._capture.release()
                self._capture = None

            self._last_frame = None

    def stop_capture(self):
        self._stop_worker()

        with self._lock:
            if self._state != CaptureState.IDLE:
                self._transition(CaptureState.IDLE)

    def pause_capture(self):
        with self._lock:
            if self._state == CaptureState.PAUSED:
                return

            self._transition(CaptureState.PAUSED)

    def resume_capture(self):
        with self._lock:
            if self._state == CaptureState.PAUSED:
                self._transition(CaptureState.CAPTURING)
                return

            if self._state == CaptureState.CAPTURING:
                return

            logger.warning(
                f"Cannot resume capture from state: {self._state.name}")
            raise InvalidStateTransition(self._state, CaptureState.CAPTURING)

    def read_frame(self):
        with self._lock:
            if self._state == CaptureState.PAUSED:
                return self._last_frame

            if self._state != CaptureState.CAPTURING:
                return None

            return self._last_frame

    def set_device(self, device):
        if not device:
            raise ValueError("Invalid device")

        self.stop_capture()
        self.current_device = device

    def set_window(self, window):
        if not window:
            raise ValueError("Invalid window")

        self.stop_capture()
        self._current_window = window

    def set_window_by_title(self, title):
        for w in self.windows:
            if w.title == title:
                self.set_window(w)
                return

        raise ValueError(f"Window not found: {title}")

    # endregion

    _BACKEND_MAP = {
        "DSHOW": cv2.CAP_DSHOW,
        "MSMF": cv2.CAP_MSMF,
        "V4L2": getattr(cv2, "CAP_V4L2", None),
        "AUTO": None,
    }

    # region Capture loops
    def _capture_loop(self):
        source = self.current_device.index
        prefs = Prefs()

        backend = self._BACKEND_MAP.get(prefs.capture_backend)
        if backend is not None:
            cap = cv2.VideoCapture(source, backend)
        else:
            cap = cv2.VideoCapture(source)

        if not self._running:
            cap.release()
            return

        config = {
            cv2.CAP_PROP_FRAME_WIDTH: prefs.video_capture_width,
            cv2.CAP_PROP_FRAME_HEIGHT: prefs.video_capture_height,
            cv2.CAP_PROP_FPS: prefs.capture_fps,
            cv2.CAP_PROP_BUFFERSIZE: 1,
        }

        if prefs.capture_codec:
            fourcc = cv2.VideoWriter_fourcc(*prefs.capture_codec)
            config[cv2.CAP_PROP_FOURCC] = fourcc

        logger.debug("[CvControl] Applying capture config...")
        config_info = ""
        for prop, val in config.items():
            ok = cap.set(prop, val)
            curr = cap.get(prop)
            status = "OK" if ok else "FAIL"
            name = self._prop_name(prop)

            if prop == cv2.CAP_PROP_FOURCC:
                config_info += (
                    f"  {name:20s} req={_fourcc_str(val):>6s}"
                    f"  actual={_fourcc_str(curr):>6s}  [{status}]\n")
            else:
                config_info += (
                    f"  {name:20s} req={val:>8.1f}"
                    f"  actual={curr:>8.1f}  [{status}]\n")

        logger.debug(
            f"[CvControl] Config requested vs accepted:\n{config_info}")

        # Log the actual final state of the camera after all settings applied
        final_info = ""
        for prop_id, name in sorted(self._PROP_NAMES.items()):
            val = cap.get(prop_id)
            if val == -1.0 and prop_id not in config:
                continue
            if prop_id == cv2.CAP_PROP_FOURCC:
                final_info += f"  {name:20s} = {_fourcc_str(val)}\n"
            else:
                final_info += f"  {name:20s} = {val}\n"

        logger.debug(
            f"[CvControl] Actual camera state:\n{final_info}")

        if not cap.isOpened():
            cap.release()
            logger.error(f"[CvControl] Couldn't open source: {source}")

            with self._lock:
                self._transition(CaptureState.ERROR)

            self.capture_started.emit(False)

            return

        with self._lock:
            self._capture = cap
            self._transition(CaptureState.CAPTURING)

        self.capture_started.emit(True)

        while self._running:
            with self._lock:
                state = self._state

            if state == CaptureState.PAUSED:
                time.sleep(Const.FRAME_INTERVAL)
                continue
            if state != CaptureState.CAPTURING:
                break

            # read() blocks until a new frame is available — no sleep needed
            ret, frame = cap.read()

            if not ret:
                continue

            if Const.DEBUG_MODE:
                self._frame_count += 1
                now = time.time()
                if now - self._fps_last >= 1.0:
                    self._fps = self._frame_count
                    self._frame_count = 0
                    self._fps_last = now
                h, w = frame.shape[:2]
                overlay_lines = [
                    f"{w}x{h} | FPS: {self._fps:.1f}",
                    f"FOURCC: {_fourcc_str(cap.get(cv2.CAP_PROP_FOURCC))}",
                ]
                y = 30
                for line in overlay_lines:
                    cv2.putText(frame, line, (10, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    y += 30

            with self._lock:
                self._last_frame = frame

    def _window_capture_loop(self):
        hwnd = self._current_window.handle
        title = self._current_window.title
        cap = None

        while self._running:
            is_minimized = win32gui.IsIconic(hwnd)

            if is_minimized:
                cap = self._handle_window_minimized(cap)
                time.sleep(0.25)
                continue

            if self._state == CaptureState.MINIMIZED:
                cap = self._handle_window_restored(title)
                if cap is None:
                    return
                continue

            if cap is None:
                cap = self._open_window_capture(title)
                if cap is None:
                    return
                continue

            with self._lock:
                state = self._state

            if state == CaptureState.PAUSED:
                time.sleep(Const.FRAME_INTERVAL)
                continue

            if state != CaptureState.CAPTURING:
                break

            if not self._read_window_frame(cap, title):
                return

            # WindowCapture.read() is a screenshot (non-blocking), throttle
            time.sleep(Const.WINDOW_CAPTURE_INTERVAL)

        if cap is not None:
            cap.release()

    def _handle_window_minimized(self, cap):
        """ Transition to MINIMIZED and release capture """
        with self._lock:
            if self._state != CaptureState.MINIMIZED:
                if cap is not None:
                    cap.release()
                self._transition(CaptureState.MINIMIZED)
                self.window_minimized.emit(True)

        return None

    def _handle_window_restored(self, title):
        """ Reopen capture after window is restored """
        try:
            cap = WindowCapture(title, [0, 0, 0, 0])
        except Exception as e:
            logger.error(f"[CvControl] Couldn't reopen '{title}': {e}")

            with self._lock:
                self._transition(CaptureState.ERROR)

            self.capture_started.emit(False)

            return None

        with self._lock:
            self._capture = cap
            self._transition(CaptureState.CAPTURING)

        self.window_minimized.emit(False)
        self.capture_started.emit(True)

        return cap

    def _open_window_capture(self, title):
        """Open WindowCapture for the first time """
        try:
            cap = WindowCapture(title, [0, 0, 0, 0])
        except Exception as e:
            logger.error(f"[CvControl] Couldn't open window '{title}': {e}")

            with self._lock:
                self._transition(CaptureState.ERROR)

            self.capture_started.emit(False)

            return None

        with self._lock:
            self._capture = cap
            self._transition(CaptureState.CAPTURING)

        self.capture_started.emit(True)

        return cap

    def _read_window_frame(self, cap, title):
        """ Read a frame. Returns False on fatal error """
        try:
            ret, frame = cap.read()

            if ret:
                with self._lock:
                    self._last_frame = frame

            return True
        except Exception as e:
            logger.error(f"[CvControl] Error capturing '{title}': {e}")
            with self._lock:
                self._transition(CaptureState.ERROR)
            self.capture_started.emit(False)
            return False

    # endregion


@staticmethod
def _fourcc_str(val: float) -> str:
    """ Convert FOURCC int to string, or return 'N/A' if invalid/zero """
    v = int(val)
    if v <= 0:
        return "N/A"

    return "".join(chr((v >> (8 * i)) & 0xFF) for i in range(4))

# endregion


# region Exceptions
class CaptureError(Exception):
    pass


class InvalidStateTransition(Exception):
    def __init__(self, from_state, to_state):
        super().__init__(
            f"Invalid state transition: {from_state.name} -> {to_state.name}")
        self.from_state = from_state
        self.to_state = to_state

# endregion
