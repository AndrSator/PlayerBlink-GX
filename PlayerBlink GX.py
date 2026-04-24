import os
import sys

__version__ = "1.3.0"

# Must be set before any `import cv2` in the process.
# With HW transforms enabled, MSMF can hang for minutes
# during VideoCapture open on some Windows builds.
os.environ.setdefault("OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS", "0")

# Wayland workaround - "always on top" and window-capture break
# so force X11/XCB before Qt and SDL initialize.
if sys.platform.startswith("linux"):
    os.environ.setdefault("QT_QPA_PLATFORM", "xcb")
    os.environ.setdefault("SDL_VIDEODRIVER", "x11")

# `-DEBUG` as first arg forces Constants.DEBUG_MODE on at runtime even
# when the flag is hardcoded to False. Must be applied before src.log
# gets imported (the file-handler decision happens at import time).
# Pop it so QApplication doesn't see it as a Qt switch.
if len(sys.argv) > 1 and sys.argv[1] == "-DEBUG":
    from src.constants import Constants as Const
    Const.DEBUG_MODE = True
    sys.argv.pop(1)


if __name__ == "__main__":
    from src.main import main
    main()
