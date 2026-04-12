from .window import Window, WindowCapturer, WindowEnumerator


class MacWindowEnumerator(WindowEnumerator):

    def _enumerate(self) -> list[Window]:
        raise NotImplementedError(
            "macOS window enumeration is not implemented yet")

    def is_minimized(self, window: Window) -> bool:
        raise NotImplementedError(
            "macOS window enumeration is not implemented yet")

    def open_capture(self, window: Window) -> WindowCapturer:
        raise NotImplementedError(
            "macOS window enumeration is not implemented yet")
