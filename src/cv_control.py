import os
import cv2
import time

from enum import Enum, auto
from threading import Thread, Lock

from PySide6.QtCore import QObject, Signal

from src.capture import backend as capture_backend
from src.capture import Device, Window, make_enumerator, make_window_enumerator

from src.log import logger
from src.utils import Utils
from src.constants import Constants as Const
from src.preferences import Preferences as Prefs


__version__ = "1.0.1"


# region Models and Enums
class CaptureState(Enum):
    IDLE = auto()
    LOADING = auto()
    CAPTURING = auto()
    PAUSED = auto()
    ERROR = auto()
    MINIMIZED = auto()


class CvControl(QObject):
    """ Manages video capture from devices and windows,
    and mediates state transitions """

    # Machine transitions
    _VALID_TRANSITIONS = {
        # Startup
        (CaptureState.IDLE, CaptureState.LOADING),
        (CaptureState.LOADING, CaptureState.CAPTURING),
        (CaptureState.LOADING, CaptureState.IDLE),
        (CaptureState.LOADING, CaptureState.ERROR),
        (CaptureState.ERROR, CaptureState.LOADING),

        # Pause/resume
        (CaptureState.CAPTURING, CaptureState.PAUSED),
        (CaptureState.CAPTURING, CaptureState.IDLE),
        (CaptureState.PAUSED, CaptureState.CAPTURING),
        (CaptureState.PAUSED, CaptureState.IDLE),

        # Errors
        (CaptureState.IDLE, CaptureState.ERROR),
        (CaptureState.CAPTURING, CaptureState.ERROR),
        (CaptureState.PAUSED, CaptureState.ERROR),
        (CaptureState.ERROR, CaptureState.IDLE),

        # Monitor mode
        (CaptureState.IDLE, CaptureState.MINIMIZED),
        (CaptureState.LOADING, CaptureState.MINIMIZED),
        (CaptureState.CAPTURING, CaptureState.MINIMIZED),
        (CaptureState.PAUSED, CaptureState.MINIMIZED),
        (CaptureState.MINIMIZED, CaptureState.CAPTURING),
        (CaptureState.MINIMIZED, CaptureState.IDLE),
        (CaptureState.MINIMIZED, CaptureState.ERROR),
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
    state_changed = Signal(object)

    def __init__(self):
        super().__init__()

        self._enumerator = make_enumerator()
        self._window_enumerator = make_window_enumerator()

        self._state = CaptureState.IDLE
        self._capture = None
        self._last_frame = None
        self._lock = Lock()
        self._worker = None
        self._running = False

        # Video capture devices
        self._devices: dict[str, Device] = {}
        self._current_device: Device | None = None

        # Windows (monitor mode)
        self._windows: list[Window] = []
        self._current_window: Window | None = None
        self._monitor_mode = False
        self._monitor_supported = True
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
        enumerated = self._enumerator.list_devices()
        fresh: dict[str, Device] = {dev.uid: dev for dev, _ in enumerated}

        self._devices = fresh

        if self.current_device is None or \
                self.current_device.uid not in self._devices:
            self.current_device = next(iter(self._devices.values()), None)

        logger.debug(
            self._devices and f"[CvControl] Available devices: {[
                str(d) for d in self._devices.values()]}"
            or "No capture devices found")

    def set_next_device(self):
        self._set_device_by_offset(1)

    def set_prev_device(self):
        self._set_device_by_offset(-1)

    def _set_device_by_offset(self, offset: int):
        if not self._devices or len(self._devices) <= 1:
            return

        uids = list(self._devices.keys())
        try:
            curr = uids.index(self.current_device.uid)
        except (ValueError, AttributeError):
            curr = 0

        next_uid = uids[(curr + offset) % len(uids)]
        self.set_device(self._devices[next_uid])
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
        current_pid = os.getpid()

        try:
            self._windows = self._window_enumerator.list_windows(
                blacklist=self._blacklist,
                exclude_pids=[current_pid],
            )
            self._monitor_supported = True
        except NotImplementedError:
            logger.debug(
                "[CvControl] Window monitoring not implemented on this "
                "platform")
            self._windows = []
            self._monitor_supported = False
            return
        except Exception as e:
            logger.error(f"[CvControl] Failed to enumerate windows: {e}")
            self._windows = []
            self._monitor_supported = False
            return

        logger.debug(
            self._windows and f"[CvControl] Available windows: {[
                str(w) for w in self._windows]}" or "No windows found")

    def refresh_windows(self):
        self.setup_windows()
        return self.windows

    def toggle_monitor_mode(self):
        if not self._monitor_supported:
            self.monitor_mode = False
            logger.warning(
                "[CvControl] Monitor mode is not supported on this platform.")
            return

        self.monitor_mode = not self.monitor_mode

        return self.monitor_mode

    # endregion

    # region State machines
    @property
    def state(self):
        return self._state

    def start_capture(self):
        logger.debug(
            f"[CvControl] start_capture: state={self._state.name} "
            f"monitor_mode={self._monitor_mode} "
            f"current_device={self._current_device} "
            f"current_window={self._current_window}")
        self._stop_worker()

        with self._lock:
            if self._state == CaptureState.CAPTURING:
                logger.debug(
                    "[CvControl] start_capture: already CAPTURING, noop")
                return

            if self._state == CaptureState.PAUSED:
                logger.debug(
                    "[CvControl] start_capture: resuming from PAUSED")
                self._transition(CaptureState.CAPTURING)
                return

            if self.monitor_mode:
                if self.current_window is None:
                    logger.error(
                        "[CvControl] start_capture: no current_window")
                    self._transition(CaptureState.ERROR)
                    self.capture_started.emit(False)
                    return

                target_loop = self._window_capture_loop
            else:
                if self.current_device is None:
                    logger.error(
                        "[CvControl] start_capture: no current_device")
                    self._transition(CaptureState.ERROR)
                    self.capture_started.emit(False)
                    return

                target_loop = self._capture_loop

            self._transition(CaptureState.LOADING)

        self._running = True
        self._worker = Thread(target=target_loop, daemon=True)
        self._worker.start()
        logger.debug(
            f"[CvControl] start_capture: worker thread started "
            f"({target_loop.__name__})")

    def _transition(self, target):
        if self._state == target:
            return

        if (self._state, target) not in self._VALID_TRANSITIONS:
            raise InvalidStateTransition(self._state, target)

        logger.debug(
            f"[CvControl] Transition: "
            f"{self._state.name} -> {target.name}")
        self._state = target
        self.state_changed.emit(target)

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

    # region Capture loops
    def _capture_loop(self):
        device = self.current_device
        logger.debug(
            "[CvControl] _capture_loop starting for device "
            f"uid={device.uid!r} name={device.name!r}")

        com_initialized = False
        if Const.PLATFORM_WINDOWS:
            try:
                import comtypes
                comtypes.CoInitialize()
                com_initialized = True
                logger.debug("[CvControl] CoInitialize() succeeded on worker")
            except Exception as e:
                logger.warning(
                    f"[CvControl] CoInitialize() failed: {e}")

        try:
            self._run_capture_loop(device)
        finally:
            if com_initialized:
                try:
                    import comtypes
                    comtypes.CoUninitialize()
                    logger.debug(
                        "[CvControl] CoUninitialize() on worker exit")
                except Exception:
                    pass

    def _run_capture_loop(self, device):
        source = self._enumerator.resolve_index(device.uid)
        logger.debug(
            f"[CvControl] resolve_index({device.uid!r}) -> {source}")

        if source is None:
            logger.error(
                f"[CvControl] Device no longer available: {device}")

            with self._lock:
                self._transition(CaptureState.ERROR)

            self.capture_started.emit(False)
            return

        prefs = Prefs()
        effective_backend, backend_flag = capture_backend.resolve(
            prefs.capture_backend)

        if effective_backend != prefs.capture_backend.upper():
            logger.warning(
                f"[CvControl] Backend '{prefs.capture_backend}' is not valid "
                f"on this platform; falling back to '{effective_backend}'")

        logger.debug(
            f"[CvControl] Backend: requested={prefs.capture_backend!r} "
            f"effective={effective_backend!r} cv2_flag={backend_flag}")
        logger.debug(
            f"[CvControl] Opening cv2.VideoCapture(source={source}, "
            f"backend={effective_backend})")

        if backend_flag is not None:
            cap = cv2.VideoCapture(source, backend_flag)
        else:
            cap = cv2.VideoCapture(source)

        logger.debug(
            f"[CvControl] cv2.VideoCapture constructed: "
            f"isOpened={cap.isOpened()} "
            f"backendName={cap.getBackendName() if cap.isOpened() else 'N/A'}")

        if not self._running:
            logger.debug(
                "[CvControl] _running went False during open, releasing")
            cap.release()
            return

        if not cap.isOpened():
            cap.release()
            logger.error(
                f"[CvControl] Couldn't open source: index={source} "
                f"backend={effective_backend} "
                f"device={device}")

            with self._lock:
                self._transition(CaptureState.ERROR)

            self.capture_started.emit(False)

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
                    f"  {name:20s} req={Utils.fourcc_str(val):>6s}"
                    f"  actual={Utils.fourcc_str(curr):>6s}  [{status}]\n")
            else:
                config_info += (
                    f"  {name:20s} req={val:>8.1f}"
                    f"  actual={curr:>8.1f}  [{status}]\n")

        logger.debug(
            f"[CvControl] Config requested vs accepted:\n{config_info}")

        if capture_backend.DEBUG_CAPTURE_PROPS:
            final_info = ""
            for prop_id, name in sorted(self._PROP_NAMES.items()):
                val = cap.get(prop_id)

                if val == -1.0 and prop_id not in config:
                    continue

                val_str = f"{Utils.fourcc_str(val)
                             if prop_id == cv2.CAP_PROP_FOURCC
                             else val}"
                final_info += f"  {name:20s} = {val_str}\n"

            logger.debug(
                f"[CvControl] Actual camera state:\n{final_info}")

        with self._lock:
            self._capture = cap

        logger.debug(
            f"[CvControl] Entering read loop for {device.name} "
            f"(still LOADING, waiting for first frame)")

        consecutive_failures = 0
        first_frame_received = False
        MAX_FAILURES_BEFORE_LOG = 30

        while self._running:
            with self._lock:
                state = self._state

            if state == CaptureState.PAUSED:
                time.sleep(capture_backend.FRAME_INTERVAL)
                continue

            if state not in (CaptureState.CAPTURING, CaptureState.LOADING):
                break

            ret, frame = cap.read()

            if not ret:
                consecutive_failures += 1
                if consecutive_failures == 1 or \
                        consecutive_failures % MAX_FAILURES_BEFORE_LOG == 0:
                    logger.warning(
                        f"[CvControl] cap.read() returned ret=False "
                        f"(count={consecutive_failures}) isOpened="
                        f"{cap.isOpened()}")
                continue

            if consecutive_failures:
                logger.debug(
                    f"[CvControl] Read recovered after "
                    f"{consecutive_failures} failures")
                consecutive_failures = 0

            if not first_frame_received:
                first_frame_received = True
                logger.debug(
                    f"[CvControl] First frame received from {device.name} "
                    f"({frame.shape[1]}x{frame.shape[0]})")
                with self._lock:
                    self._transition(CaptureState.CAPTURING)
                self.capture_started.emit(True)

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
                    f"FOURCC: {Utils.fourcc_str(
                        cap.get(cv2.CAP_PROP_FOURCC))}",
                ]
                y = 30
                for line in overlay_lines:
                    cv2.putText(
                        frame, line, (10, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    y += 30

            with self._lock:
                self._last_frame = frame

    def _window_capture_loop(self):
        window = self._current_window
        cap = None

        while self._running:
            is_minimized = self._window_enumerator.is_minimized(window)

            if is_minimized:
                cap = self._handle_window_minimized(cap)
                time.sleep(0.25)
                continue

            if self._state == CaptureState.MINIMIZED:
                cap = self._handle_window_restored(window)
                if cap is None:
                    return
                continue

            if cap is None:
                cap = self._open_window_capture(window)
                if cap is None:
                    return
                continue

            with self._lock:
                state = self._state

            if state == CaptureState.PAUSED:
                time.sleep(capture_backend.FRAME_INTERVAL)
                continue

            if state not in (CaptureState.CAPTURING, CaptureState.LOADING):
                break

            if not self._read_window_frame(cap, window):
                return

            time.sleep(capture_backend.WINDOW_CAPTURE_INTERVAL)

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

    def _handle_window_restored(self, window):
        """ Reopen capture after window is restored.

        Window capture is effectively instant (BitBlt / XGetImage), so we
        transition straight to CAPTURING here without passing through
        LOADING — there is no noticeable startup cost to report.
        """
        try:
            cap = self._window_enumerator.open_capture(window)
        except Exception as e:
            logger.error(f"[CvControl] Couldn't reopen '{window.title}': {e}")

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

    def _open_window_capture(self, window):
        """ Open a WindowCapturer for the first time.

        Transitions LOADING -> CAPTURING directly because window capture
        starts instantly.
        """
        try:
            cap = self._window_enumerator.open_capture(window)
        except Exception as e:
            logger.error(
                f"[CvControl] Couldn't open window '{window.title}': {e}")

            with self._lock:
                self._transition(CaptureState.ERROR)

            self.capture_started.emit(False)

            return None

        with self._lock:
            self._capture = cap
            self._transition(CaptureState.CAPTURING)

        self.capture_started.emit(True)

        return cap

    def _read_window_frame(self, cap, window):
        """ Read a frame. Returns False on fatal error """
        try:
            ret, frame = cap.read()

            if ret:
                with self._lock:
                    self._last_frame = frame

            return True
        except Exception as e:
            logger.error(
                f"[CvControl] Error capturing '{window.title}': {e}")
            with self._lock:
                self._transition(CaptureState.ERROR)
            self.capture_started.emit(False)
            return False

    # endregion

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
