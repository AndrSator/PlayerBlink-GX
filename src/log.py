import logging

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
