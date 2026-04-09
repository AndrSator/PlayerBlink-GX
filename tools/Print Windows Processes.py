import sys

try:
    import win32gui
except ImportError:
    exit()


if sys.platform != 'win32':
    exit()

windows = []


def callback(hwnd, _):
    if not win32gui.IsWindowVisible(hwnd):
        return

    title = win32gui.GetWindowText(hwnd)
    if not title:
        return
    windows.append(title)


win32gui.EnumWindows(callback, None)


print("\n".join(f"{w}" for w in windows))
input("Press Enter to exit...")
