from typing import Any
from abc import ABC, abstractmethod

import numpy as np

from src.constants import Constants as Const
from src.log import logger


class Window:
    """ Represents a capturable desktop window.

    The native handle is kept private and is only meant to be consumed by
    the platform-specific WindowEnumerator/WindowCapturer that created the
    Window. Consumers should identify windows by uid/title/pid instead.
    """

    def __init__(self, uid: str, title: str, pid: int, native: Any):
        self._uid = uid
        self._title = title
        self._pid = pid
        self._native = native

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def title(self) -> str:
        return self._title

    @property
    def pid(self) -> int:
        return self._pid

    @property
    def native(self) -> Any:
        """ Platform-specific handle (HWND, X11 window ID, etc.).

        Only the platform implementation of WindowEnumerator should use this.
        """
        return self._native

    def __str__(self):
        return f"{self._title} ({self._pid})"

    def __eq__(self, other):
        return isinstance(other, Window) and self._uid == other._uid

    def __hash__(self):
        return hash(self._uid)


class WindowCapturer(ABC):
    """ Reads frames from a single window.

    Implementations mirror the subset of cv2.VideoCapture used by the capture
    loop: read() returns (success, frame) and release() frees resources.
    """

    @abstractmethod
    def read(self) -> tuple[bool, np.ndarray | None]:
        ...

    @abstractmethod
    def release(self) -> None:
        ...


class WindowEnumerator(ABC):
    """ Lists desktop windows and opens capture sessions against them """

    @abstractmethod
    def _enumerate(self) -> list[Window]:
        """ Platform-specific raw enumeration (unfiltered) """

    @abstractmethod
    def is_minimized(self, window: Window) -> bool:
        ...

    @abstractmethod
    def open_capture(self, window: Window) -> WindowCapturer:
        ...

    def list_windows(
        self,
        blacklist: list[str] | None = None,
        exclude_pids: list[int] | None = None,
    ) -> list[Window]:
        """ Enumerate windows and apply cross-platform filters.

        blacklist: case-insensitive substrings to reject by title
        exclude_pids: PIDs to skip (e.g. the app's own process)
        """

        raw = self._enumerate()
        logger.debug(
            f"[WindowEnum] list_windows: raw={len(raw)} "
            f"blacklist={len(blacklist) if blacklist else 0} "
            f"exclude_pids={exclude_pids}")

        result: list[Window] = []
        bl_lower = [b.lower() for b in blacklist] if blacklist else []

        for w in raw:
            if not w.title:
                logger.debug(f"[WindowEnum]   skip {w.uid!r}: no title")
                continue

            if exclude_pids and w.pid in exclude_pids:
                logger.debug(
                    f"[WindowEnum]   skip {w.uid!r}: pid {w.pid} "
                    f"in exclude list")
                continue

            if bl_lower and any(b in w.title.lower() for b in bl_lower):
                logger.debug(
                    f"[WindowEnum]   skip {w.uid!r}: blacklisted "
                    f"title={w.title!r}")
                continue

            logger.debug(f"[WindowEnum]   keep {w.uid!r}: {w.title!r}")
            result.append(w)

        logger.debug(
            f"[WindowEnum] list_windows: {len(result)} windows after filter")
        return result


def make_window_enumerator() -> WindowEnumerator:
    """ Instantiate the window enumerator for the current platform """

    if Const.PLATFORM_WINDOWS:
        from .window_win import WindowsWindowEnumerator
        return WindowsWindowEnumerator()

    if Const.PLATFORM_LINUX:
        from .window_linux import LinuxWindowEnumerator
        return LinuxWindowEnumerator()

    if Const.PLATFORM_MAC:
        from .window_mac import MacWindowEnumerator
        return MacWindowEnumerator()

    raise NotImplementedError(
        "No window enumerator available for this platform")
