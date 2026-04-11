from pathlib import Path


class Constants:
    """ Application-wide constants and default values """

    DEBUG_MODE = True

    # Logic
    DOUBLE_BLINK_MARGIN_SECONDS = 0.7
    FRAME_CORRECTION = 1.018  # Switch game tick period
    PKMN_BLINK_INTERVAL_MIN = 3
    PKMN_BLINK_INTERVAL_MAX = 12
    PKMN_BLINK_INTERVAL_OFFSET = 0.285
    BLINK_BIT_MASK = 0xE  # 0b1110
    BLINK_TYPE_MASK = 0x03  # 0b0011
    MAX_23BIT_INT = (1 << 23) - 1  # 0x7fffff, used to normalize RNG to float

    # Capture
    MSMF_HW_TRANSFORMS = False  # Disable MSMF hardware transforms (latency)
    WINDOW_CAPTURE_INTERVAL = 1 / 60  # Throttle for screenshot-based capture

    # Capture defaults
    DF_CAPTURE_BACKEND = "DSHOW"  # DSHOW, MSMF, V4L2, or AUTO
    DF_CAPTURE_FPS = 60
    DF_CAPTURE_CODEC = "MJPG"  # MJPG, YUY2, H264, or empty for auto
    DF_DISPLAY_POLL_MS = 0  # 0 = match capture FPS, >0 = fixed ms interval
    DF_GPU_RENDERING = True  # True = GPU scales via OpenGL, False = CPU scales

    # Tracking
    BLINKS_REQUIRED_TRACKING = 40
    BLINKS_REQUIRED_REIDENTIFY = 7
    BLINKS_REQUIRED_REIDENTIFY_NOISY = 20
    BLINKS_REQUIRED_TRACKING_TIDSID = 64
    FRAME_INTERVAL = 1 / 60
    REIDENT_MIN = 0
    REIDENT_MAX = 2_000_000

    # Visuals
    OFFSET_ADVANCES_PREDICTION = 15
    MAX_ADVANCES_HISTORY = 4
    ICON_DEFAULT_SIZE = 24
    ICON_DEFAULT_SIZE_SMALL = 16
    ICON_DEFAULT_SIZE_BIG = 42

    # Animations
    SCROLL_ANIMATION_DURATION = 180

    # Other
    MIN_IMG_SIZE_BYTES = 10
    MAX_IMG_SIZE_BYTES = 5 * 1024 * 1024  # 5MB
    SUPPORTED_FORMATS = ("PNG", "JPEG", "BMP")
    VALID_OPENCV_BACKENDS = ("DSHOW", "MSMF", "V4L2", "AUTO")

    # Default values
    DF_LANG = "en"
    DF_LOG_LEVEL = "INFO"
    DF_DISPLAY_MIN_WIDTH = 1920
    DF_DISPLAY_MIN_HEIGHT = 1080
    DF_COUNTDOWN_DURATION_TICKS = 10

    DF_REIDENT_MIN_VAL = 0
    DF_REIDENT_MAX_VAL = 1_000_000
    DF_REIDENT_STEP_VAL = 1000.0
    DF_THRESHOLD = 0.9

    # Paths
    BASE_DIR = Path(__file__).parent.parent
    RESOURCE_DIR = BASE_DIR / "resources"
    PREFERENCES_DIR = BASE_DIR / "preferences"
    IMAGES_DIR = BASE_DIR / "images"
    THEMES_DIR = BASE_DIR / "themes"

    FONTS_DIR = RESOURCE_DIR / "fonts"
    ICONS_DIR = RESOURCE_DIR / "icons"
    EYES_DIR = IMAGES_DIR / "eyes"
    CONFIGS_DIR = BASE_DIR / "configs"

    # Files
    JSON_PREFERENCES_FILE = PREFERENCES_DIR / "preferences.json"
    QSS_FILE = RESOURCE_DIR / "style.qss"
    BL_FILE = PREFERENCES_DIR / "monitor_mode_blacklist.txt"
    DARK_THEME_FILE = THEMES_DIR / "default_dark.ini"
