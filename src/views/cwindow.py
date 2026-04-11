from PySide6.QtWidgets import QWidget, QPushButton, QApplication
from PySide6.QtCore import Qt, QEvent

from .icon_utils import setup_icons
from ..constants import Constants as Const
from ..ui.cwindow_ui import Ui_CustomWindow


_BORDER_MARGIN = 5

_ICONS = {
    "switch_always_on_top": {
        "icon": "keep.svg"
    },
    "btn_close": {
        "icon": "close.svg"
    },
    "btn_minimize": {
        "icon": "minimize.svg"
    },
}


class CWindow(QWidget, Ui_CustomWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self._on_top = False

        self._icons_path = Const.ICONS_DIR

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)

        self.topbar.mousePressEvent = self._topbar_press
        self.topbar.mouseMoveEvent = self._topbar_move

        self.btn_close.clicked.connect(self.close)
        self.btn_minimize.clicked.connect(self.showMinimized)
        self.switch_always_on_top.clicked.connect(self.toggle_always_on_top)

        self._icons_ready = False

    def showEvent(self, event):
        super().showEvent(event)
        if not self._icons_ready:
            self._icons_ready = True
            self._setup_icons()
            for btn in self.findChildren(QPushButton):
                btn.setAttribute(Qt.WA_Hover, True)
            self.setMinimumSize(self.minimumSizeHint())
            QApplication.instance().installEventFilter(self)

    def closeEvent(self, event):
        QApplication.instance().removeEventFilter(self)
        super().closeEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseMove and not event.buttons():
            local = self.mapFromGlobal(event.globalPosition().toPoint())

            if self.rect().contains(local):
                self.setCursor(self._cursor_for_edges(
                    self._detect_qt_edges(local)))
            else:
                self.unsetCursor()

        return False

    def _setup_icons(self):
        setup_icons(self, _ICONS, self._icons_path,
                    Const.ICON_DEFAULT_SIZE_SMALL)

    def toggle_always_on_top(self):
        self._on_top = not self._on_top
        self.setWindowFlag(Qt.WindowStaysOnTopHint, self._on_top)
        self.switch_always_on_top.setProperty("active", self._on_top)
        self.switch_always_on_top.style().unpolish(self.switch_always_on_top)
        self.switch_always_on_top.style().polish(self.switch_always_on_top)
        self.show()

    # Topbar drag (native)
    def _topbar_press(self, event):
        if event.button() == Qt.LeftButton:
            self.windowHandle().startSystemMove()

    def _topbar_move(self, event):
        pass

    # # Edge detection & cursor
    def _detect_qt_edges(self, pos):
        m = _BORDER_MARGIN
        w, h = self.width(), self.height()
        edges = Qt.Edge(0)

        if pos.x() <= m:
            edges |= Qt.LeftEdge
        elif pos.x() >= w - m:
            edges |= Qt.RightEdge

        if pos.y() <= m:
            edges |= Qt.TopEdge
        elif pos.y() >= h - m:
            edges |= Qt.BottomEdge

        return edges

    def _cursor_for_edges(self, edges):
        tl = Qt.LeftEdge | Qt.TopEdge
        br = Qt.RightEdge | Qt.BottomEdge
        tr = Qt.RightEdge | Qt.TopEdge
        bl = Qt.LeftEdge | Qt.BottomEdge

        if edges in (tl, br):
            return Qt.SizeFDiagCursor
        if edges in (tr, bl):
            return Qt.SizeBDiagCursor
        if edges & (Qt.LeftEdge | Qt.RightEdge):
            return Qt.SizeHorCursor
        if edges & (Qt.TopEdge | Qt.BottomEdge):
            return Qt.SizeVerCursor
        return Qt.ArrowCursor

    # Native resize
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            edges = self._detect_qt_edges(event.pos())
            if edges:
                self.windowHandle().startSystemResize(edges)

    def mouseMoveEvent(self, event):
        if not event.buttons():
            self.setCursor(self._cursor_for_edges(
                self._detect_qt_edges(event.pos())))
