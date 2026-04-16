from superqt import QToggleSwitch
from superqt.switch._toggle_switch import QStyleOptionToggleSwitch


class CToggleSwitch(QToggleSwitch):
    def _vertical_offset(self, opt: QStyleOptionToggleSwitch) -> int:
        return (self.height() - opt.switch_height) // 2
