# PlayerBlink GX

## Overview

Improved version of Player Blink with enhanced UI, error handling, and detection accuracy. Some features may be broken or not implemented yet.

> Based on the original Project_Xs by niart120 and Player Blink by lincoln-lm.

---

## Features

* Friendly user interface with a customizable theme.
* Visual display for A press, countdown start timing (previously known as timeline), target advance along other stuff.
* Improved accuracy using a calibrated tick instead of an empirical value.
* Displays predictions of future advances along with their blinks (from player or NPC).
* Easy control and editing of the ROI and screenshot area using the mouse.
* Image gallery with simple management for blink tracking.
* Better error handling and feedback through logs.

---

## Requirements

* Python 3.12+ (May work on previous versions) 
* OpenCV
* Pillow
* Qt (PySide6)


---

## Installation

### Windows
```bash
git clone https://github.com/AndrSator/PlayerBlink-GX
cd PlayerBlink-GX
pip install -r requirements.txt
```

### Linux (Debian 13+ / Ubuntu 24.04+)
```bash
git clone https://github.com/AndrSator/PlayerBlink-GX
cd PlayerBlink-GX

# Build toolchain + system libs for window capture (D-Bus + GStreamer/PipeWire)
sudo apt install build-essential python3-dev python3-venv pkg-config \
    libdbus-1-dev libgirepository-2.0-dev libcairo2-dev \
    libxcb-cursor0 \
    gir1.2-gstreamer-1.0 gir1.2-gst-plugins-base-1.0 \
    gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    gstreamer1.0-pipewire

python3 -m venv venv
source venv/bin/activate
pip install -r requirements_linux.txt
```

> **Ubuntu note:** If `libgirepository-2.0-dev` is not found (Ubuntu < 24.04),
> use `libgirepository1.0-dev` instead.

---

## Usage

Run the GUI:

```bash
python "PlayerBlink GX.py"
```

### Linux / Wayland notes

Most modern Linux distros default to a **Wayland** session. PlayerBlink GX
works under Wayland but there are some differences compared to X11/Windows:

- **Window capture (monitor mode)** uses `xdg-desktop-portal` + PipeWire,
  the same API that OBS uses. When you activate monitor mode and start
  capture, the **compositor's native window picker** will appear. The
  required system packages are installed during the Linux installation
  steps above.

- **"Always on top" (pin window)** does not work under native Wayland
  because the compositor controls window stacking. To force PlayerBlink GX
  to run under XWayland where this feature works, launch it with:
  ```bash
  QT_QPA_PLATFORM=xcb python "PlayerBlink GX.py"
  ```

---

## License

This project is licensed under the MIT License.

It includes code derived from Project_Xs by niart120 and lincoln-lm
