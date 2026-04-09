# BlinkSeed

## Overview

Improved version of Player Blink with enhanced UI, error handling, and detection accuracy.

> Based on the original Project_Xs by niart120 and Player Blink by lincoln-lm.

---

## Features

* Real-time blink detection using computer vision
* RNG state recovery from blink sequences
* Advance tracking and timeline support
* Configurable detection settings
* GUI-based workflow for easier interaction

---

## Requirements

* Python 3.7+
* Git
* OpenCV (installed via requirements)

---

## Installation

```bash
git clone https://github.com/yourusername/blinkseed.git
cd blinkseed
pip install -r requirements.txt
```

---

## Usage

Run the GUI:

```bash
python ./src/player_blink_gui.py
```

---

## Main Functions

### Blink Monitoring

Records blink sequences to determine the current RNG state and starts tracking advances.

### Reidentify

Uses a shorter blink sequence to resync your RNG state from known seeds.

### TID/SID Mode

Captures blink data during the intro sequence to calculate trainer IDs.

### Timeline

Provides countdown-based RNG manipulation for events like starters and legendaries.

---

## Configuration

The tool allows full customization of detection parameters:

* Detection area (X, Y, Width, Height)
* Eye recognition threshold
* NPC and Pokémon blink behavior
* Timeline delays and advance offsets

---

## Notes

* Accuracy depends heavily on proper eye image selection and threshold tuning
* Different scenarios (starters, legendaries, overworld) may require different configs

---

## Disclaimer

This software is provided for educational and research purposes. Use at your own discretion.

---

## License

This project is licensed under the MIT License.

It includes code derived from Project_Xs by niart120.
