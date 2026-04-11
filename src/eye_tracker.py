import io
import cv2
import time
import numpy as np

from PIL import Image
from enum import Enum, auto
from threading import Thread

from PySide6.QtCore import QObject, Signal

from src.constants import Constants as Const
from src.log import logger

__version__ = "1.0.0"


# region Models and Enums
class BlinkType(Enum):
    IDLE = 0x00
    SINGLE = 0x01
    DOUBLE = 0x02


class TrackingState(Enum):
    IDLE = auto()
    TRACKING = auto()
    PREVIEW = auto()


class EyeTracker(QObject):
    """ Tracks eye blinks from a video source using template matching """

    # type, interval, count, total
    blink_detected = Signal(int, int, int, int)
    # blinks, intervals, raw_intervals, offset, end_time
    tracking_finished = Signal(list, list, list, float, float)
    tracking_error = Signal(str)
    # match_loc: (is_matching, x, y, eye_w, eye_h) in frame coords
    match_updated = Signal(bool, int, int, int, int)

    def __init__(self):
        super().__init__()

        self._state = TrackingState.IDLE
        self._threshold = Const.DF_THRESHOLD
        self._size = Const.BLINKS_REQUIRED_TRACKING
        self._frame_correction = Const.FRAME_CORRECTION

        self._img_pattern_sample = None  # raw bytes (PNG/JPEG/BMP)
        self._eye_gray = None  # cv2 grayscale array (cached)
        self._tracking_area = None  # (x, y, w, h) in frame coords

        self._cv_control = None
        self._worker = None
        self._running = False

        self._calibrated_tick = None  # measured tick rate from last tracking

    # region Properties
    @property
    def state(self):
        return self._state

    def is_tracking(self):
        return self._state == TrackingState.TRACKING

    def is_idle(self):
        return self._state == TrackingState.IDLE

    def is_preview(self):
        return self._state == TrackingState.PREVIEW

    def is_active(self):
        return self._state in (TrackingState.TRACKING, TrackingState.PREVIEW)

    @property
    def frame_correction(self):
        return self._frame_correction

    @frame_correction.setter
    def frame_correction(self, value):
        if value <= 0:
            raise ValueError(f"Frame correction must be > 0. {value}")
        self._frame_correction = value

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        if not (0 < value <= 1):
            raise ValueError(f"Threshold must be between 0 and 1. {value}")
        self._threshold = value

    @property
    def tracking_area(self):
        return self._tracking_area

    @tracking_area.setter
    def tracking_area(self, value):
        if value is not None:
            if len(value) != 4 or any(v < 0 for v in value):
                raise ValueError(
                    f"tracking_area must be (x, y, w, h). {value}")
        self._tracking_area = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value < 1:
            raise ValueError(f"Size must be >= 1. {value}")
        self._size = value

    @property
    def calibrated_tick(self):
        return self._calibrated_tick

    @property
    def img_pattern_sample(self):
        return self._img_pattern_sample

    @img_pattern_sample.setter
    def img_pattern_sample(self, value):
        if not value:
            raise ValueError("Image empty or corrupted")

        size = len(value)
        if size > Const.MAX_IMG_SIZE_BYTES:
            raise ValueError(f"Image too large ({size * 1024} KB)")

        if size < Const.MIN_IMG_SIZE_BYTES:
            raise ValueError("Image too small to be valid")

        try:
            img = Image.open(io.BytesIO(value))
            img.verify()

            img = Image.open(io.BytesIO(value))

            if img.format not in Const.SUPPORTED_FORMATS:
                msg = f"Unsupported image format: {img.format} "\
                    f"(allowed: {Const.SUPPORTED_FORMATS})"
                raise ValueError(msg)

        except Exception as e:
            logger.error(f"[EyeTracker] Invalid image: {e}")
            raise ValueError(f"Invalid image: {e}")

        self._img_pattern_sample = value

        # Cache the grayscale cv2 version
        arr = np.frombuffer(value, dtype=np.uint8)
        self._eye_gray = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)

    # endregion

    # region Tracking control
    def start_tracking(self, cv_control):
        self._start(cv_control, TrackingState.TRACKING)

    def start_preview(self, cv_control):
        self._start(cv_control, TrackingState.PREVIEW)

    def _start(self, cv_control, mode):
        if self._state != TrackingState.IDLE:
            return

        if self._eye_gray is None:
            self.tracking_error.emit("No eye pattern loaded")
            return

        if self._tracking_area is None:
            self.tracking_error.emit("No tracking area defined")
            return

        if not cv_control.is_capturing():
            self.tracking_error.emit("Capture is not active")
            return

        self._cv_control = cv_control
        self._state = mode
        self._running = True
        self._worker = Thread(target=self._tracking_loop, daemon=True)
        self._worker.start()

    def stop(self):
        self._running = False
        if self._worker is not None:
            self._worker.join(timeout=5)
            self._worker = None
        self._state = TrackingState.IDLE

    # endregion

    # region Calibration
    @staticmethod
    def calibrate_tick_rate(intervals, blink_times):
        """Estimate the game tick period from observed blink data using
        ordinary least squares regression on (tick_index, wall_clock).

        Each blink is mapped to its cumulative tick index (blink 0 at the
        origin) and its perf_counter timestamp. The slope of the best-fit
        line is the tick period in seconds; its standard error gives a
        1-sigma uncertainty.

        Designed to be reusable: a manual calibration button can collect
        a longer (intervals, blink_times) sequence and call this directly.

        Args:
            intervals: list of integer tick counts between consecutive
                blinks. intervals[0] is the start-of-recording artifact
                and is ignored, matching the legacy two-point calibration.
            blink_times: list of perf_counter timestamps, one per blink.
                Must be the same length as intervals.

        Returns:
            (tick_rate, std_error) tuple of floats in seconds, or
            (None, None) if there is not enough data to fit a line.
        """
        n = len(blink_times)
        if n < 3 or len(intervals) != n:
            return None, None

        # Cumulative tick index of each blink (blink 0 at origin)
        tick_indices = np.zeros(n, dtype=np.float64)
        for i in range(1, n):
            tick_indices[i] = tick_indices[i - 1] + intervals[i]

        if tick_indices[-1] <= 0:
            return None, None

        x = tick_indices
        y = np.asarray(blink_times, dtype=np.float64)

        x_mean = x.mean()
        y_mean = y.mean()
        dx = x - x_mean
        sxx = float((dx * dx).sum())
        if sxx <= 0:
            return None, None

        slope = float((dx * (y - y_mean)).sum() / sxx)
        intercept = y_mean - slope * x_mean

        residuals = y - (slope * x + intercept)
        sigma2 = float((residuals * residuals).sum()) / (n - 2)
        se_slope = float(np.sqrt(sigma2 / sxx))

        return slope, se_slope

    # endregion

    # region Tracking loop
    def _tracking_loop(self):
        threshold = self._threshold
        target_size = self._size
        preview_only = self._state == TrackingState.PREVIEW

        blinks = []
        intervals = []
        blink_times = []  # perf_counter per blink, for calibration
        raw_intervals = []  # float seconds (for munchlax recovery)
        prev_time = time.perf_counter()
        prev_roi = None
        offset_time = 0.0
        detect_state = BlinkType.IDLE

        while self._running:
            if not preview_only and len(blinks) >= target_size \
                    and detect_state == BlinkType.IDLE:
                break

            # Re-read on every iteration so ROI / pattern changes
            # made from the UI take effect in real time
            eye = self._eye_gray
            area = self._tracking_area
            if eye is None or area is None:
                time.sleep(0.001)
                continue

            roi_x, roi_y, roi_w, roi_h = area
            eye_h, eye_w = eye.shape[:2]

            frame = self._cv_control.read_frame()
            if frame is None:
                time.sleep(0.001)
                continue

            roi = frame[roi_y:roi_y + roi_h, roi_x:roi_x + roi_w]
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

            if prev_roi is not None \
                    and roi_gray.shape == prev_roi.shape \
                    and (roi_gray == prev_roi).all():
                time.sleep(0.001)
                continue

            prev_roi = roi_gray.copy()
            now = time.perf_counter()

            if roi_gray.shape[0] < eye_h or roi_gray.shape[1] < eye_w:
                logger.warning(
                    f"[EyeTracker] ROI ({roi_gray.shape[1]}x"
                    f"{roi_gray.shape[0]}) smaller than eye template "
                    f"({eye_w}x{eye_h}), skipping frame")
                time.sleep(0.001)
                continue

            res = cv2.matchTemplate(roi_gray, eye, cv2.TM_CCOEFF_NORMED)
            _, match, _, max_loc = cv2.minMaxLoc(res)

            is_blinking = 0.01 < match < threshold

            if is_blinking:
                self.match_updated.emit(False, 0, 0, 0, 0)

                if detect_state == BlinkType.IDLE:
                    interval = (now - prev_time) / self._frame_correction

                    if not preview_only:
                        blinks.append(0)
                        intervals.append(round(interval))
                        raw_intervals.append(now - prev_time)
                        blink_times.append(now)

                        if len(intervals) == target_size:
                            offset_time = now

                    detect_state = BlinkType.SINGLE
                    prev_time = now

                    self.blink_detected.emit(
                        0, round(interval),
                        len(blinks) if not preview_only else -1,
                        target_size)

                # Allow a small margin for double blink detection to account
                # for timing inaccuracies
                elif (detect_state == BlinkType.SINGLE and
                      now - prev_time >
                      (1.0 - Const.DOUBLE_BLINK_MARGIN_SECONDS)):
                    if not preview_only:
                        blinks[-1] = 1

                    detect_state = BlinkType.DOUBLE
                    self.blink_detected.emit(
                        1, 0,
                        len(blinks) if not preview_only else -1,
                        target_size)
            else:
                abs_x = roi_x + max_loc[0]
                abs_y = roi_y + max_loc[1]
                self.match_updated.emit(True, abs_x, abs_y, eye_w, eye_h)

            if (detect_state != BlinkType.IDLE and
                    now - prev_time > Const.DOUBLE_BLINK_MARGIN_SECONDS):
                detect_state = BlinkType.IDLE

        self._state = TrackingState.IDLE
        self.match_updated.emit(False, 0, 0, 0, 0)

        if not preview_only and len(blinks) >= target_size:
            end_time = time.perf_counter()

            # Calibrate tick rate via linear regression on blink data
            tick_rate, se_tick = self.calibrate_tick_rate(
                intervals, blink_times)
            if tick_rate is not None:
                self._calibrated_tick = tick_rate
                logger.info(
                    f"[EyeTracker] Calibrated tick_rate="
                    f"{tick_rate * 1000:.3f}ms/tick "
                    f"(\u00b1{se_tick * 1000:.3f}ms) "
                    f"from {len(blink_times)} blinks")

            self.tracking_finished.emit(
                blinks, intervals, raw_intervals, offset_time, end_time)

    # endregion

# endregion
