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

```bash
git clone https://github.com/AndrSator/PlayerBlink-GX
cd PlayerBlink-GX
pip install -r requirements.txt
```

---

## Usage

Run the GUI:

```bash
python "PlayerBlink GX.py"
```

---

## License

This project is licensed under the MIT License.

It includes code derived from Project_Xs by niart120 and lincoln-lm
