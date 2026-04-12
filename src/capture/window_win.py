import numpy as np

import win32con
import win32gui
import win32process
import win32ui

from src.log import logger

from .window import Window, WindowCapturer, WindowEnumerator


# Default chrome offsets used to crop the title bar and side borders out
# of the captured frame. These match the legacy WindowCapture defaults so
# downstream coordinates remain consistent.
_BORDER_PIXELS = 8
_TITLEBAR_PIXELS = 31


class WindowsWindowCapturer(WindowCapturer):
    """ Captures frames from a Win32 window via GDI BitBlt.

    Geometry is recomputed on every ``read()`` so that resizing the target
    window mid-capture is handled transparently — the next frame will
    match the new dimensions instead of cropping/stretching the old size.
    The cost is a single ``GetWindowRect`` call per frame (~microseconds).
    """

    def __init__(self, window: Window):
        self._hwnd = window.native
        self._title = window.title

    def _current_geometry(self) -> tuple[int, int, int, int]:
        """ Return (capture_w, capture_h, crop_x, crop_y) for the window now """
        rect = win32gui.GetWindowRect(self._hwnd)
        full_w = rect[2] - rect[0]
        full_h = rect[3] - rect[1]

        capture_w = max(1, full_w - (_BORDER_PIXELS * 2))
        capture_h = max(1, full_h - _TITLEBAR_PIXELS - _BORDER_PIXELS)
        return capture_w, capture_h, _BORDER_PIXELS, _TITLEBAR_PIXELS

    def read(self):
        width, height, crop_x, crop_y = self._current_geometry()

        window_dc = win32gui.GetWindowDC(self._hwnd)
        dc_object = win32ui.CreateDCFromHandle(window_dc)
        compatible_dc = dc_object.CreateCompatibleDC()
        data_bitmap = win32ui.CreateBitmap()

        try:
            data_bitmap.CreateCompatibleBitmap(dc_object, width, height)
        except win32ui.error as e:
            raise RuntimeError(
                f"Failed to pull input from window '{self._title}'. "
                f"Make sure nothing else is accessing it (stop preview "
                f"before monitoring blinks)."
            ) from e

        compatible_dc.SelectObject(data_bitmap)
        compatible_dc.BitBlt(
            (0, 0),
            (width, height),
            dc_object,
            (crop_x, crop_y),
            win32con.SRCCOPY,
        )

        # Raw GDI bitmap is BGRA 32 bits per pixel
        signed_ints_array = data_bitmap.GetBitmapBits(True)
        img = np.frombuffer(signed_ints_array, dtype=np.uint8)
        img.shape = (height, width, 4)

        # Free GDI resources
        dc_object.DeleteDC()
        compatible_dc.DeleteDC()
        win32gui.ReleaseDC(self._hwnd, window_dc)
        win32gui.DeleteObject(data_bitmap.GetHandle())

        # Drop alpha and ensure C-contiguous for OpenCV
        # See https://github.com/opencv/opencv/issues/14866
        img = np.ascontiguousarray(img[..., :3])

        return True, img

    def release(self):
        # No persistent GDI resources to release — read() handles its own.
        pass


class WindowsWindowEnumerator(WindowEnumerator):
    """ Enumerates top-level visible windows via win32gui.EnumWindows.

    The UID is the HWND stringified. HWNDs are unique within a session but
    not stable across sessions, which is fine for monitor-mode selection
    (the user picks a window while the app is running).
    """

    def _enumerate(self) -> list[Window]:
        windows: list[Window] = []

        def callback(hwnd, _):
            if not win32gui.IsWindowVisible(hwnd):
                return

            title = win32gui.GetWindowText(hwnd)
            if not title:
                return

            try:
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
            except Exception as e:
                logger.warning(
                    f"[WinWindowEnum] Failed to get pid for hwnd {hwnd}: {e}")
                return

            windows.append(
                Window(uid=str(hwnd), title=title, pid=pid, native=hwnd))

        win32gui.EnumWindows(callback, None)

        return windows

    def is_minimized(self, window: Window) -> bool:
        return bool(win32gui.IsIconic(window.native))

    def open_capture(self, window: Window) -> WindowCapturer:
        return WindowsWindowCapturer(window)
