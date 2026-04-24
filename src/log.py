import logging

from datetime import datetime
from enum import Enum
from src.constants import Constants as Const


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR

    @classmethod
    def from_string(cls, value: str):
        try:
            return cls[value.upper()].value
        except KeyError:
            return cls[Const.DF_LOG_LEVEL.upper()].value


# Logger global
logger = logging.getLogger("player_blink_gx")
logger.setLevel(LogLevel.DEBUG.value)

if not logger.handlers:
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d|%(levelname)s|%(message)s',
        datefmt='%H:%M:%S'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if Const.DEBUG_MODE:
        Const.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = Const.LOGS_DIR / f"session_{stamp}.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
