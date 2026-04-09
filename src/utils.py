from src.eye_tracker import BlinkType
from src.constants import Constants as Const


class Utils:
    @staticmethod
    def blink_from_rng(value):
        """ Extract BlinkType from a raw RNG value, or None if no blink """

        if (value & Const.BLINK_BIT_MASK) == 0:
            return BlinkType.DOUBLE if (value & 1) else BlinkType.SINGLE

        return None

    @staticmethod
    def format_time(seconds: float) -> str:
        """ Format a time value in seconds to a string HH:MM:SS.mmm """

        ms = int((seconds % 1) * 1000)
        total_seconds = int(seconds)

        s = total_seconds % 60
        m = (total_seconds // 60) % 60
        h = total_seconds // 3600

        return f"{h:02}:{m:02}:{s:02}.{ms:03}"
