import json

from PySide6.QtCore import QObject, Signal

from src.log import logger
from src.constants import Constants as Const

__version__ = "1.0.0"


class ConfigModel(QObject):
    """
    Manages RNG-manipulation config files (fossil, honey, etc.).
    Loads, validates, previews and applies config values.
    """

    config_loaded = Signal(object)   # emitted after load(); payload = self
    config_saved = Signal(str)       # emitted after save(); payload = filename

    def __init__(self, configs_dir=None):
        super().__init__()

        self._configs_dir = configs_dir or Const.CONFIGS_DIR
        self._current_file = None

        # Config fields with defaults
        self._name = ""
        self._description = ""
        self._image = "eye.png"
        self._roi = [0, 0, 0, 0]
        self._plus_one_menu_close = True
        self._final_a_press_delay = 0
        self._timeline_buffer = 0
        self._threshold = Const.DF_THRESHOLD
        self._time_delay = 0.0
        self._advance_delay = 0
        self._advance_delay_2 = 0
        self._npc = 0
        self._pkmn_npc = 0
        self._timeline_npc = 0

    # region Properties

    @property
    def current_file(self):
        return self._current_file

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"name must be a non-empty string, got {value!r}")
        self._name = value.strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError(
                f"description must be a string, got {value!r}")
        self._description = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"image must be a non-empty string, got {value!r}")
        self._image = value.strip()

    @property
    def roi(self):
        return list(self._roi)

    @roi.setter
    def roi(self, value):
        if not isinstance(value, (list, tuple)) or len(value) != 4:
            raise ValueError(
                f"roi must be a list of 4 integers, got {value!r}")

        parsed = []
        for v in value:
            if not isinstance(v, (int, float)):
                raise ValueError(
                    f"roi values must be integers, got {v!r}")
            parsed.append(int(v))

        self._roi = parsed

    @property
    def plus_one_menu_close(self):
        return self._plus_one_menu_close

    @plus_one_menu_close.setter
    def plus_one_menu_close(self, value):
        if not isinstance(value, bool):
            raise ValueError(
                f"plus_one_menu_close must be bool, got {value!r}")
        self._plus_one_menu_close = value

    @property
    def final_a_press_delay(self):
        return self._final_a_press_delay

    @final_a_press_delay.setter
    def final_a_press_delay(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(
                f"final_a_press_delay must be >= 0, got {value!r}")
        self._final_a_press_delay = int(value)

    @property
    def timeline_buffer(self):
        return self._timeline_buffer

    @timeline_buffer.setter
    def timeline_buffer(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(
                f"timeline_buffer must be >= 0, got {value!r}")
        self._timeline_buffer = int(value)

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError(
                f"threshold must be a number, got {value!r}")

        value = float(value)
        if not (0.0 <= value <= 1.0):
            raise ValueError(
                f"threshold must be between 0.0 and 1.0, got {value!r}")
        self._threshold = value

    @property
    def time_delay(self):
        return self._time_delay

    @time_delay.setter
    def time_delay(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(
                f"time_delay must be >= 0, got {value!r}")
        self._time_delay = float(value)

    @property
    def advance_delay(self):
        return self._advance_delay

    @advance_delay.setter
    def advance_delay(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(
                f"advance_delay must be >= 0, got {value!r}")
        self._advance_delay = int(value)

    @property
    def advance_delay_2(self):
        return self._advance_delay_2

    @advance_delay_2.setter
    def advance_delay_2(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(
                f"advance_delay_2 must be >= 0, got {value!r}")
        self._advance_delay_2 = int(value)

    @property
    def npc(self):
        return self._npc

    @npc.setter
    def npc(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"npc must be >= 0, got {value!r}")
        self._npc = int(value)

    @property
    def pkmn_npc(self):
        return self._pkmn_npc

    @pkmn_npc.setter
    def pkmn_npc(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"pkmn_npc must be >= 0, got {value!r}")
        self._pkmn_npc = int(value)

    @property
    def timeline_npc(self):
        return self._timeline_npc

    @timeline_npc.setter
    def timeline_npc(self, value):
        if not isinstance(value, (int, float)) or value < -1:
            raise ValueError(f"timeline_npc must be >= -1, got {value!r}")
        self._timeline_npc = int(value)

    # endregion

    # region Public API

    def list_configs(self):
        """Return sorted list of .json filenames in configs dir."""
        if not self._configs_dir.is_dir():
            logger.warning(
                f"[ConfigModel] Configs dir not found: {self._configs_dir}")
            return []

        return sorted(
            f.name for f in self._configs_dir.glob("*.json"))

    def peek_name(self, filename):
        """Read only the 'name' field from a config file without loading."""
        filepath = self._configs_dir / filename
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("name", filename)
        except Exception:
            return filename

    def load(self, filename):
        """Load a config file by filename and populate properties."""
        filepath = self._configs_dir / filename
        logger.debug(f"[ConfigModel] Loading config: {filepath}")

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"[ConfigModel] Error loading config: {e}")
            return False

        try:
            self.name = data.get("name", "")
            self.description = data.get("description", "")
            self.image = data.get("image", "eye.png")
            self.roi = data.get("roi", [0, 0, 0, 0])
            self.plus_one_menu_close = data.get(
                "plus_one_menu_close", True)
            self.final_a_press_delay = data.get(
                "final_a_press_delay", 0)
            self.timeline_buffer = data.get("timeline_buffer", 0)
            self.threshold = data.get("threshold", Const.DF_THRESHOLD)
            self.time_delay = data.get("time_delay", 0.0)
            self.advance_delay = data.get("advance_delay", 0)
            self.advance_delay_2 = data.get("advance_delay_2", 0)
            self.npc = data.get("npc", 0)
            self.pkmn_npc = data.get("pkmn_npc", 0)
            self.timeline_npc = data.get("timeline_npc", 0)
        except (ValueError, TypeError) as e:
            logger.error(f"[ConfigModel] Validation error: {e}")
            return False

        self._current_file = filename
        self.config_loaded.emit(self)
        logger.debug(f"[ConfigModel] Config loaded: {self._name}")
        return True

    def save(self, filename=None):
        """Save current config to a file. Uses current file if none given."""
        filename = filename or self._current_file
        if not filename:
            logger.error("[ConfigModel] No filename specified for save")
            return False

        filepath = self._configs_dir / filename
        logger.info(f"[ConfigModel] Saving config: {filepath}")

        data = {
            "name": self._name,
            "description": self._description,
            "image": self._image,
            "roi": self._roi,
            "plus_one_menu_close": self._plus_one_menu_close,
            "final_a_press_delay": self._final_a_press_delay,
            "timeline_buffer": self._timeline_buffer,
            "threshold": self._threshold,
            "time_delay": self._time_delay,
            "advance_delay": self._advance_delay,
            "advance_delay_2": self._advance_delay_2,
            "npc": self._npc,
            "pkmn_npc": self._pkmn_npc,
            "timeline_npc": self._timeline_npc,
        }

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"[ConfigModel] Error saving config: {e}")
            return False

        self._current_file = filename
        self.config_saved.emit(filename)
        logger.info(f"[ConfigModel] Config saved: {self._name}")
        return True

    def create(self, name):
        """Create a new config file with default values."""
        filename = f"{name}.json"
        filepath = self._configs_dir / filename

        if filepath.exists():
            logger.warning(
                f"[ConfigModel] Config already exists: {filename}")
            return None

        self._reset_defaults()
        self._name = name
        self._current_file = filename

        if self.save(filename):
            return filename

        return None

    # endregion

    def _reset_defaults(self):
        self._name = ""
        self._description = ""
        self._image = "eye.png"
        self._roi = [0, 0, 0, 0]
        self._plus_one_menu_close = True
        self._final_a_press_delay = 0
        self._timeline_buffer = 0
        self._threshold = Const.DF_THRESHOLD
        self._time_delay = 0.0
        self._advance_delay = 0
        self._advance_delay_2 = 0
        self._npc = 0
        self._pkmn_npc = 0
        self._timeline_npc = 0
        self._current_file = None
