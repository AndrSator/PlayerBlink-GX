import json

from PySide6.QtGui import QColor

from src.utils import Utils
from src.capture import backend
from src.log import logger, LogLevel
from src.constants import Constants as Const

__version__ = "1.0.1"


class Preferences:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self._filepath = Const.JSON_PREFERENCES_FILE

        self._theme = Const.DARK_THEME_FILE
        self._language = Const.DF_LANG
        self._log_level = LogLevel.INFO.value
        self._calibrated_tick = True
        self._countdown_ticks = Const.DF_COUNTDOWN_DURATION_TICKS
        self._roi_color = Const.DF_ROI_COLOR
        self._img_match_color = Const.DF_IMG_MATCH_COLOR

        # Advanced
        self._video_capture_width = Const.DF_DISPLAY_MIN_WIDTH
        self._video_capture_height = Const.DF_DISPLAY_MIN_HEIGHT
        self._capture_backend = backend.default_name()
        self._capture_fps = backend.DF_CAPTURE_FPS
        self._capture_codec = backend.DF_CAPTURE_CODEC
        self._gpu_rendering = Const.DF_GPU_RENDERING
        self._display_poll_ms = Const.DF_DISPLAY_POLL_MS
        self._smooth_scaling = True

        self.load()

    # region Properties
    @property
    def theme(self):
        return self._theme

    @theme.setter
    def theme(self, value):
        if not isinstance(value, str):
            raise ValueError(f"theme must be a string value. {value!r}")

        theme_path = Const.THEMES_DIR / value
        if not theme_path.is_file():
            logger.warning(
                f"[Preferences] Theme file not found: {theme_path!r}."
                " Using default theme.")
            theme_path = Const.DARK_THEME_FILE

        if not theme_path.is_file():
            logger.error(
                f"[Preferences] Default theme file not found: {theme_path!r}")
            return

        logger.info(f"[Preferences] Setting theme to: {theme_path!r}")
        self._theme = theme_path

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        if isinstance(value, str):
            self._language = value

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, value):
        if isinstance(value, int):
            self._log_level = value

        elif isinstance(value, str):
            try:
                self._log_level = LogLevel[value.upper()].value
            except KeyError:
                self._log_level = LogLevel.INFO.value
                logger.warning(
                    f"[Preferences] Unknow log level {value}. "
                    f"Setting log level to: {LogLevel(self._log_level).name}")
        else:
            raise ValueError(
                f"log_level must be a string or integer value. {value!r}")

        logger.info(
            f"[Preferences] Setting log level to: "
            f"{LogLevel(self._log_level).name}")
        logger.setLevel(self._log_level)

    @property
    def calibrated_tick(self):
        return self._calibrated_tick

    @calibrated_tick.setter
    def calibrated_tick(self, value):
        if not isinstance(value, bool):
            raise ValueError(
                f"calibrated_tick must be a boolean value. {value!r}")

        self._calibrated_tick = value

    @property
    def countdown_ticks(self):
        return self._countdown_ticks

    @countdown_ticks.setter
    def countdown_ticks(self, value):
        if not isinstance(value, int):
            raise ValueError(
                f"countdown_ticks must be a integer value. {value!r}")

        max = Const.DF_COUNTDOWN_DURATION_TICKS_MAX
        if value > max:
            value = Const.DF_COUNTDOWN_DURATION_TICKS_MAX
            logger.warning(
                f"[Preferences] countdown_ticks exceeds default max ({max}). "
                f"Set to {value}")

        self._countdown_ticks = value

    @property
    def roi_color(self):
        return self._roi_color

    @roi_color.setter
    def roi_color(self, value):
        c = Utils.parse_hex_color(value)
        if not c:
            raise ValueError(f"Invalid color: {value}")

        self._roi_color = c.name(QColor.NameFormat.HexArgb)

    @property
    def img_match_color(self):
        return self._img_match_color

    @img_match_color.setter
    def img_match_color(self, value):
        c = Utils.parse_hex_color(value)
        if not c:
            raise ValueError(f"Invalid color: {value}")

        self._img_match_color = c.name(QColor.NameFormat.HexArgb)

    @property
    def video_capture_width(self):
        return self._video_capture_width

    @video_capture_width.setter
    def video_capture_width(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(
                f"video_capture_width must be positive. {value!r}")

        self._video_capture_width = float(value)

    @property
    def video_capture_height(self):
        return self._video_capture_height

    @video_capture_height.setter
    def video_capture_height(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(
                f"video_capture_height must be positive. {value!r}")

        self._video_capture_height = float(value)

    @property
    def capture_backend(self):
        return self._capture_backend

    @capture_backend.setter
    def capture_backend(self, value):
        valid = backend.all_names()
        value = str(value).upper()

        if value not in valid:
            default = backend.default_name()
            logger.warning(
                f"[Preferences] Invalid backend '{value}', "
                f"using default: {default}")
            value = default

        self._capture_backend = value

    @property
    def capture_fps(self):
        return self._capture_fps

    @capture_fps.setter
    def capture_fps(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError(
                f"capture_fps must be a positive number. {value!r}")

        self._capture_fps = int(value)

    @property
    def capture_codec(self):
        return self._capture_codec

    @capture_codec.setter
    def capture_codec(self, value):
        if not isinstance(value, str):
            raise ValueError(
                f"capture_codec must be a string. {value!r}")

        self._capture_codec = value.upper()

    @property
    def display_poll_ms(self):
        return self._display_poll_ms

    @display_poll_ms.setter
    def display_poll_ms(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(
                f"display_poll_ms must be >= 0. {value!r}")

        self._display_poll_ms = int(value)

    @property
    def gpu_rendering(self):
        return self._gpu_rendering

    @gpu_rendering.setter
    def gpu_rendering(self, value):
        if not isinstance(value, bool):
            raise ValueError(
                f"gpu_rendering must be a boolean value. {value!r}")
        self._gpu_rendering = value

    @property
    def smooth_scaling(self):
        return self._smooth_scaling

    @smooth_scaling.setter
    def smooth_scaling(self, value):
        if not isinstance(value, bool):
            raise ValueError(
                f"smooth_scaling must be a boolean value. {value!r}")

        self._smooth_scaling = value
    # endregion

    # region Load/Save
    def load(self):
        logger.info("Loading preferences from %s", self._filepath)

        try:
            with open(self._filepath, "r") as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Error loading preferences: {e}")
            return

        self.theme = data.get("theme", self._theme)
        self.language = data.get("language", self._language)
        self.log_level = data.get("log_level", self._log_level)
        self.calibrated_tick = data.get(
            "calibrated_tick", self._calibrated_tick)
        self.countdown_ticks = data.get(
            "countdown_ticks", self._countdown_ticks)
        self.roi_color = data.get("roi_color", self._roi_color)
        self.img_match_color = data.get(
            "img_match_color", self._img_match_color)

        # OpenCV settings (advanced.opencv section, with top-level fallback)
        opencv = data.get("advanced", {}).get("opencv", {})
        self.video_capture_width = opencv.get(
            "width", data.get(
                "video_capture_width", self._video_capture_width))
        self.video_capture_height = opencv.get(
            "height", data.get(
                "video_capture_height", self._video_capture_height))
        self.capture_backend = opencv.get(
            "backend", self._capture_backend)
        self.capture_fps = opencv.get(
            "cap_prop_fps", self._capture_fps)
        self.capture_codec = opencv.get(
            "codec", self._capture_codec)
        self.display_poll_ms = opencv.get(
            "display_poll_ms", self._display_poll_ms)
        self.gpu_rendering = opencv.get(
            "gpu_rendering", self._gpu_rendering)
        self.smooth_scaling = data.get(
            "smooth_scaling", self._smooth_scaling)

        self.logg_config()

    def save(self):
        logger.info("Saving preferences to %s", self._filepath)
        theme = self._theme.name if hasattr(self._theme, "name") \
            else str(self._theme)
        data = {
            "theme": theme,
            "language": self._language,
            "log_level": LogLevel(self._log_level).name,
            "smooth_scaling": self._smooth_scaling,
            "calibrated_tick": self._calibrated_tick,
            "countdown_ticks": self._countdown_ticks,
            "roi_color": self._roi_color,
            "img_match_color": self._img_match_color,
            "advanced": {
                "opencv": {
                    "width": self._video_capture_width,
                    "height": self._video_capture_height,
                    "backend": self._capture_backend,
                    "cap_prop_fps": self._capture_fps,
                    "codec": self._capture_codec,
                    "display_poll_ms": self._display_poll_ms,
                    "gpu_rendering": self._gpu_rendering,
                }
            },
        }

        try:
            with open(self._filepath, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Error saving preferences: {e}")

    def logg_config(self):
        str_preferences = "[Preferences] Current Preferences:\n"
        str_preferences += (
            f"- Theme: {self._theme}\n"
            f"- Language: {self._language}\n"
            f"- Log Level: {LogLevel(self._log_level).name}\n"
            f"- Calibrated Tick: {self._calibrated_tick}\n"
            f"- Smooth Scaling: {self._smooth_scaling}\n"
            f"- Video Capture Width: {self._video_capture_width}\n"
            f"- Video Capture Height: {self._video_capture_height}\n"
            f"- Capture Backend: {self._capture_backend}\n"
            f"- Capture FPS: {self._capture_fps}\n"
            f"- Capture Codec: {self._capture_codec}\n"
            f"- Display Poll MS: {self._display_poll_ms}\n"
            f"- GPU Rendering: {self._gpu_rendering}"
        )

        logger.info(str_preferences)

    # endregion
