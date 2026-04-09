import os
import sys
import json

from PIL import Image
from pathlib import Path
from datetime import datetime

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication, QLabel, QScrollArea, \
    QVBoxLayout, QWidget, QDialog, QDialogButtonBox, QLineEdit

from ..log import logger

_RESOURCE_MIN_ITEM_SIZE = 50
_SUPPORTED_FORMATS = (".png", ".jpeg", ".bmp")


class Resource:
    def __init__(self, file_path):
        self.path = Path(file_path)
        self._image_info = None
        self._stat = None

    def _get_stat(self):
        if self._stat is None:
            self._stat = self.path.stat()
        return self._stat

    @property
    def name(self):
        return self.path.name

    @property
    def extension(self):
        return self.path.suffix.lower()

    @property
    def size(self):
        return self._get_stat().st_size

    @property
    def created(self):
        return self._get_stat().st_ctime

    @property
    def modified(self):
        return self._get_stat().st_mtime

    @property
    def width(self):
        return self._load_image_info().get("width")

    @property
    def height(self):
        return self._load_image_info().get("height")

    @property
    def resolution(self):
        return f"{self.width}x{self.height}"

    @property
    def mode(self):
        return self._load_image_info().get("mode")

    @property
    def format(self):
        return self._load_image_info().get("format")

    @property
    def dpi(self):
        return self._load_image_info().get("dpi")

    @property
    def created_str(self):
        return datetime.fromtimestamp(self.created).strftime("%Y-%m-%d %H:%M")

    def __str__(self):
        return f"{self.name} | {self.resolution} | {self.created_str}"

    def _load_image_info(self):
        if self._image_info is not None:
            return self._image_info

        try:
            with Image.open(self.path) as img:
                self._image_info = {
                    "width": img.width,
                    "height": img.height,
                    "mode": img.mode,
                    "format": img.format.capitalize(),
                    "dpi": img.info.get("dpi"),
                }
        except Exception:
            self._image_info = {}

        return self._image_info


class _FlowContainer(QWidget):
    def __init__(self, max_columns, spacing=6,
                 min_item_width=_RESOURCE_MIN_ITEM_SIZE,
                 min_item_height=_RESOURCE_MIN_ITEM_SIZE):
        super().__init__()
        self._max_columns = max_columns
        self._min_item_width = min_item_width
        self._min_item_height = min_item_height
        self._spacing = spacing
        self._items = []
        self._on_row_height_changed = None
        self._scrollbar_margin = 0

    def add_item(self, widget, relayout=True):
        widget.setParent(self)
        self._items.append(widget)
        if relayout:
            self._relayout()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._relayout()

    def _relayout(self):
        if not self._items:
            return

        available = self.width() - self._scrollbar_margin
        if available <= 0:
            return

        sp = self._spacing
        cols = max(1, min(
            self._max_columns,
            (available + sp) // (self._min_item_width + sp)
        ))

        item_w = (available - sp * (cols - 1)) / cols
        scale = item_w / self._min_item_width
        item_h = self._min_item_height * scale

        for i, widget in enumerate(self._items):
            row, col = divmod(i, cols)
            x = col * (item_w + sp)
            y = row * (item_h + sp)
            widget.setGeometry(int(x), int(y), int(item_w), int(item_h))
            widget.show()

        rows = (len(self._items) + cols - 1) // cols
        total_h = int(rows * item_h + (rows - 1) * sp)
        self.setMinimumHeight(total_h)

        if self._on_row_height_changed:
            self._on_row_height_changed(int(item_h))


class GalleryItem(QLabel):
    def __init__(self, resource=None, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(False)
        self.setMinimumWidth(_RESOURCE_MIN_ITEM_SIZE)
        self.setMinimumHeight(_RESOURCE_MIN_ITEM_SIZE)
        self.setProperty("selected", False)

        self._resource = resource
        self._source_pixmap = None

        if resource and hasattr(resource, "path"):
            self._load_pixmap(str(resource.path))

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, value):
        self._resource = value
        if value and hasattr(value, "path"):
            self._load_pixmap(str(value.path))

    def _load_pixmap(self, path):
        pm = QPixmap(path)
        if not pm.isNull():
            self._source_pixmap = pm
            self._apply_scaled_pixmap()

    def _apply_scaled_pixmap(self):
        if self._source_pixmap:
            target = self.size().boundedTo(self._source_pixmap.size())
            scaled = self._source_pixmap.scaled(
                target, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.setPixmap(scaled)

    def set_selected(self, selected):
        self.setProperty("selected", selected)
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            container = self._find_gallery_container()
            if container:
                container._on_item_clicked(self)
        super().mousePressEvent(event)

    def _find_gallery_container(self):
        p = self.parent()
        while p:
            if isinstance(p, GalleryContainer):
                return p
            p = p.parent()
        return None

    def reload(self):
        if self._resource and hasattr(self._resource, "path"):
            self._load_pixmap(str(self._resource.path))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._apply_scaled_pixmap()


class GalleryContainer(QWidget):
    _SCROLLBAR_PADDING = 6

    # Signals
    selection_changed = Signal(object)

    def __init__(self, res_dir, columns=12, spacing=6,
                 min_item_width=_RESOURCE_MIN_ITEM_SIZE,
                 min_item_height=_RESOURCE_MIN_ITEM_SIZE):
        super().__init__()
        self._res_dir = res_dir

        _outer_layout = QVBoxLayout(self)
        _outer_layout.setContentsMargins(0, 0, 0, 0)

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        _outer_layout.addWidget(self._scroll)

        self._lbl_resource_info = QLabel()
        _outer_layout.addWidget(self._lbl_resource_info)

        self._container = _FlowContainer(
            columns, spacing,
            min_item_width, min_item_height
        )
        self._scroll.setWidget(self._container)
        self._container._on_row_height_changed = self._update_scroll_min_height

        self._selected_item = None

        self._setup_items()

    @property
    def selected_resource(self):
        return self._selected_item.resource if self._selected_item else None

    @property
    def columns(self):
        return self._container._max_columns

    @columns.setter
    def columns(self, value):
        if value < 1:
            raise ValueError("columns must be >= 1")
        self._container._max_columns = value
        self._container._relayout()

    def _on_item_clicked(self, item):
        if self._selected_item is item:
            self._selected_item.set_selected(False)
            self._selected_item = None
            self._set_item_info()
            self.selection_changed.emit(None)
            return

        self._select_item(item)

    def select_by_name(self, name):
        """Select a gallery item by resource filename."""
        for item in self._container._items:
            if item.resource and item.resource.name == name:
                self._select_item(item)
                return True
        return False

    def _select_item(self, item):
        if self._selected_item:
            self._selected_item.set_selected(False)
        item.set_selected(True)
        self._selected_item = item
        self._set_item_info()
        self.selection_changed.emit(item.resource)

    def _set_item_info(self):
        if self._selected_item is None:
            self._lbl_resource_info.setText("")
            return

        res = self._selected_item.resource
        self._lbl_resource_info.setText(str(res))

    def _update_scroll_min_height(self, row_height):
        self._scroll.setMinimumHeight(row_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        vbar = self._scroll.verticalScrollBar()
        margin = self._SCROLLBAR_PADDING if vbar.isVisible() else 0
        if self._container._scrollbar_margin != margin:
            self._container._scrollbar_margin = margin
            self._container._relayout()

    def add_resource(self, resource):
        item = GalleryItem(resource)
        self._container.add_item(item)
        self._select_item(item)
        return item

    def reload_selected(self):
        if self._selected_item is not None:
            self._selected_item.reload()

    def remove_selected(self):
        if self._selected_item is None:
            return None

        resource = self._selected_item.resource
        self._selected_item.hide()
        self._container._items.remove(self._selected_item)
        self._selected_item.deleteLater()
        self._selected_item = None
        self._lbl_resource_info.setText("")
        self._container._relayout()
        self.selection_changed.emit(None)

        return resource

    def add_widget(self, widget):
        self._container.add_item(widget)

    def _setup_items(self):
        if not os.path.isdir(self._res_dir):
            raise ValueError(f"Invalid resource directory: {self._res_dir}")

        for filename in sorted(os.listdir(self._res_dir)):
            ext = os.path.splitext(filename)[1].lower()
            if ext not in _SUPPORTED_FORMATS:
                continue

            file_path = os.path.join(self._res_dir, filename)
            if os.path.isfile(file_path):
                resource = Resource(file_path)
                item = GalleryItem(resource)
                self._container.add_item(item, relayout=False)

        self._container._relayout()

    def _clear_items(self):
        for item in self._container._items:
            item.hide()
            item.deleteLater()
        self._container._items.clear()
        self._selected_item = None
        self._lbl_resource_info.setText("")

    def reload_items(self):
        self._clear_items()
        self._setup_items()


class FileNameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowTitle("Create new resource")
        self.setFixedSize(250, 120)

        _layout = QVBoxLayout(self)

        self._label = QLabel("File name:")
        _layout.addWidget(self._label)

        self._line_edit = QLineEdit()
        self._line_edit.setPlaceholderText("EyePattern")
        _layout.addWidget(self._line_edit)

        self._buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        _layout.addWidget(self._buttons)

        self._ok_button = self._buttons.button(QDialogButtonBox.Ok)
        self._ok_button.setEnabled(False)

        self._line_edit.textChanged.connect(self._on_text_changed)

    def get_name(self):
        return self._line_edit.text().strip()

    def _on_text_changed(self, text):
        text = text.strip()
        ok_button = self._buttons.button(QDialogButtonBox.Ok)
        ok_button.setEnabled(bool(text))


if __name__ == "__main__":
    app = QApplication()

    window = QWidget()
    window.setWindowTitle("GalleryItem Playground")
    window.resize(500, 400)

    root_layout = QVBoxLayout(window)
    root_layout.setSpacing(12)
    root_layout.setContentsMargins(16, 16, 16, 16)

    res_dir = os.path.join("images", "eyes")
    gc = GalleryContainer(res_dir)

    root_layout.addWidget(gc)

    ini_path = "themes/default_dark.ini"
    qss_path = "resources/style.qss"
    font_paths = font_paths = ["resources/fonts/RobotoMono-Medium.ttf"]

    try:
        for font in font_paths:
            QFontDatabase.addApplicationFont(font)

        with open(ini_path, "r") as f:
            theme = json.load(f)

        with open(qss_path, "r") as f:
            qss = f.read()

        for key, value in theme.items():
            qss = qss.replace(f"{{{{{key}}}}}", value)

        app.setStyleSheet(qss)
    except Exception as e:
        logger.error(f"Error loading theme: {e}")

    window.show()
    sys.exit(app.exec())
