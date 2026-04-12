""" Central configuration for the OpenCV capture subsystem.

Owns:
 * the list of known backends (name, cv2 flag, supported platforms);
 * platform-aware backend resolution (:func:`resolve`) and default
   selection (:func:`default_name`);
 * capture-pipeline runtime knobs and preference defaults used by the
   capture loop and by :class:`src.preferences.Preferences`.

Everything video-capture related lives in one place so that strings like
``"DSHOW"``, ``"MJPG"`` or ``1/60`` are declared exactly once.
"""
import cv2

from dataclasses import dataclass

from src.constants import Constants as Const


# Capture runtime knobs
# Dump every camera property via cap.get() after opening the device. Can
# add 500+ ms to startup on some webcams over DShow, so it stays opt-in
# even in DEBUG_MODE.
DEBUG_CAPTURE_PROPS = False

# Sleep between iterations of the window (screenshot-based) capture loop.
# Window capture is non-blocking so we need to throttle explicitly.
WINDOW_CAPTURE_INTERVAL = 1 / 60

# Sleep the capture loops take while PAUSED, waiting for the state to
# change. Not latency-sensitive because no frame is being delivered.
FRAME_INTERVAL = 1 / 60


# Preference defaults
DF_CAPTURE_FPS = 60
DF_CAPTURE_CODEC = "MJPG"  # MJPG, YUY2, H264, or empty for AUTO


@dataclass(frozen=True)
class Backend:
    name: str
    flag: int | None  # cv2.CAP_* constant, or None for "auto-select"
    platforms: frozenset[str]


_WIN = "windows"
_LNX = "linux"
_MAC = "mac"
_ALL_PLATFORMS = frozenset({_WIN, _LNX, _MAC})


BACKENDS: tuple[Backend, ...] = (
    Backend("AUTO", None, _ALL_PLATFORMS),
    Backend("DSHOW", cv2.CAP_DSHOW, frozenset({_WIN})),
    Backend("MSMF", cv2.CAP_MSMF, frozenset({_WIN})),
    Backend("V4L2", getattr(cv2, "CAP_V4L2", None), frozenset({_LNX})),
)


def _current_platform() -> str:
    if Const.PLATFORM_WINDOWS:
        return _WIN

    if Const.PLATFORM_LINUX:
        return _LNX

    if Const.PLATFORM_MAC:
        return _MAC

    return "unknown"


def all_names() -> tuple[str, ...]:
    """ Every backend name known to the app, regardless of platform """
    return tuple(b.name for b in BACKENDS)


def valid_names(platform: str | None = None) -> tuple[str, ...]:
    """ Backend names valid on the given platform (default: current) """
    platform = platform or _current_platform()
    return tuple(b.name for b in BACKENDS if platform in b.platforms)


def default_name(platform: str | None = None) -> str:
    """ The preferred default backend for a platform.

    Picked as the first non-AUTO backend valid on the platform, so the app
    ships with a sensible value without anyone having to hardcode "DSHOW"
    or "V4L2" at call sites.
    """

    platform = platform or _current_platform()

    for b in BACKENDS:
        if b.name == "AUTO":
            continue
        if platform in b.platforms:
            return b.name

    return "AUTO"


def resolve(requested: str,
            platform: str | None = None) -> tuple[str, int | None]:
    """ Resolve a backend name to ``(effective_name, cv2_flag)``.

    Falls back to AUTO if the requested backend is not valid on the current
    platform. Returning the effective name (not only the flag) lets callers
    log what actually happened.
    """

    platform = platform or _current_platform()
    requested_upper = str(requested).upper()

    for b in BACKENDS:
        if b.name == requested_upper and platform in b.platforms:
            return b.name, b.flag

    # Not valid on this platform → AUTO fallback.
    for b in BACKENDS:
        if b.name == "AUTO":
            return b.name, b.flag

    return "AUTO", None
