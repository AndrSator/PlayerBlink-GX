import sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QColor, QIcon, Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, \
    QHBoxLayout, QLabel

from ..constants import Constants as Const


_BLINK_ICON_MAP = [
    "",                       # IDLE
    "visibility.svg",         # SINGLE
    "visibility_filled.svg",  # DOUBLE
]

_TIMER_ICON_MAP = [
    "timer.svg",
    "hdr_auto.svg",  # looks like A button!
]


class AdvanceLabel(QWidget):
    def __init__(self, text="",
                 prepend_icon: int | None = None,
                 append_icon: int | None = None,
                 icon_size=16, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Icon
        self._prepend_icon_size = icon_size
        self._prepend_icon_label = QLabel()
        self._prepend_icon_label.setFixedSize(icon_size, icon_size)
        self._prepend_icon_label.setScaledContents(True)
        self._prepend_icon_label.setAttribute(Qt.WA_TranslucentBackground)

        # Label
        self._text_label = QLabel(text)
        self._text_label.setAlignment(Qt.AlignCenter)
        self._text_label.setFixedHeight(42)

        # Icon
        self._append_icon_size = icon_size
        self._append_icon_label = QLabel()
        self._append_icon_label.setFixedSize(icon_size, icon_size)
        self._append_icon_label.setScaledContents(True)
        self._append_icon_label.setAttribute(Qt.WA_TranslucentBackground)

        layout.addWidget(self._prepend_icon_label)
        layout.addWidget(self._text_label)
        layout.addWidget(self._append_icon_label)

        if prepend_icon is not None:
            self.prepend_icon(prepend_icon)
        if append_icon is not None:
            self.append_icon(append_icon)

    # region Qt overrides

    def setProperty(self, name: str, value):
        super().setProperty(name, value)
        self._text_label.setProperty(name, value)

    def setAlignment(self, alignment):
        self._text_label.setAlignment(alignment)

    def repolish(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self._text_label.style().unpolish(self._text_label)
        self._text_label.style().polish(self._text_label)

    def setText(self, text: str):
        self._text_label.setText(text)

    def text(self) -> str:
        return self._text_label.text()

    def setProgress(self, value):
        self.progress = value
        self.update()

    def getActiveColor(self):
        return self._color_text

    def setActiveColor(self, color):
        self._color_text = QColor(color)
        self.update()

    def getBorderColor(self):
        return self._color_border

    def setBorderColor(self, color):
        self._color_border = QColor(color)
        self.update()

    def getBackgroundColor(self):
        return self._color_background

    def setBackgroundColor(self, color):
        self._color_background = QColor(color)
        self.update()

    # endregion

    def prepend_icon(self, icon):
        if isinstance(icon, int) and 0 <= icon < len(_TIMER_ICON_MAP):
            path = str(Const.ICONS_DIR / _TIMER_ICON_MAP[icon])
            pixmap = QIcon(path).pixmap(
                QSize(self._prepend_icon_size, self._prepend_icon_size))
            self._prepend_icon_label.setPixmap(pixmap)
            return

        self._prepend_icon_label.clear()

    def append_icon(self, icon):
        # Append icons only support blink types
        if icon is not None and icon != 0:
            path = str(Const.ICONS_DIR / _BLINK_ICON_MAP[icon])
            pixmap = QIcon(path).pixmap(
                QSize(self._append_icon_size, self._append_icon_size))
            self._append_icon_label.setPixmap(pixmap)
            return

        self._append_icon_label.clear()


if __name__ == "__main__":
    app = QApplication()

    window = QWidget()
    window.setWindowTitle("IconLabel Playground")
    window.resize(400, 200)

    root_layout = QVBoxLayout(window)
    root_layout.setSpacing(12)
    root_layout.setContentsMargins(16, 16, 16, 16)

    lbl1 = AdvanceLabel("Circle", prepend_icon=0)
    lbl2 = AdvanceLabel("Circle Fill", append_icon=0)

    root_layout.addWidget(lbl1)
    root_layout.addWidget(lbl2)
    root_layout.addStretch()

    window.show()
    sys.exit(app.exec())
