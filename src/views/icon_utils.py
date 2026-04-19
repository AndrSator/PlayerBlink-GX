import os

from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QIcon, QIconEngine, QPainter, QPixmap, QPalette
from PySide6.QtCore import Qt, QByteArray, QObject, QEvent, QSize, \
    QRect, QRectF

from ..constants import Constants as Const


# Default fill used by Google Material SVG icons
_DEFAULT_SVG_FILL = 'fill="#e3e3e3"'


class _SvgIconEngine(QIconEngine):
    """ Custom QIconEngine that re-rasterizes a (recolored) SVG at the
    exact size Qt asks for on each paint.

    Going through QIcon.addPixmap stores fixed-size pixmaps that Qt has
    to re-scale for any other request, and the device pixel ratio
    metadata is brittle through that path (the cached entry is keyed by
    physical size and the DPR can be lost on cache hits, which is what
    was making the icons appear at twice their logical size on HiDPI
    screens). With a custom engine the SVG is rendered fresh at the
    requested physical size and Qt tags the result with the right DPR
    afterwards, so the result is always sharp and at the correct
    logical size.
    """

    def __init__(self, svg_data, normal_color, disabled_color=None):
        super().__init__()
        self._svg_data = svg_data
        self._normal_color = normal_color
        self._disabled_color = disabled_color or normal_color

    def clone(self):
        return _SvgIconEngine(
            self._svg_data, self._normal_color, self._disabled_color)

    def actualSize(self, size, mode, state):
        # The SVG can be rendered at any size, so always honor the
        # requested size verbatim.
        return size

    def _color_for_mode(self, mode):
        if mode == QIcon.Mode.Disabled:
            return self._disabled_color
        return self._normal_color

    def paint(self, painter, rect, mode, state):
        colored = self._svg_data.replace(
            _DEFAULT_SVG_FILL, f'fill="{self._color_for_mode(mode)}"')
        renderer = QSvgRenderer(QByteArray(colored.encode()))
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        renderer.render(painter, QRectF(rect))
        painter.restore()

    def pixmap(self, size, mode, state):
        # Qt calls this with `size` already multiplied by the device
        # pixel ratio (so it is in physical pixels). The outer QIcon
        # code tags the returned pixmap with the right DPR, which gives
        # the correct logical size on HiDPI screens.
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        self.paint(
            painter, QRect(0, 0, size.width(), size.height()), mode, state)
        painter.end()
        return pixmap


class _ButtonIconResizer(QObject):
    """ Adjusts a button's iconSize as the button is resized.

    The actual SVG rasterization is done on demand by `_SvgIconEngine`,
    so this filter only has to keep `setIconSize` in sync with the
    button's current size, capped by `max_size`.
    """

    def __init__(self, btn, max_size=None):
        super().__init__(btn)
        self._max_size = max_size

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Resize:
            side = min(obj.width(), obj.height())
            if self._max_size:
                side = min(side, self._max_size)
            obj.setIconSize(QSize(side, side))
        return False


def get_icon_colors(btn):
    role = btn.foregroundRole()
    palette = btn.palette()
    normal = palette.color(QPalette.ColorGroup.Normal, role).name()
    disabled = palette.color(QPalette.ColorGroup.Disabled, role).name()
    return normal, disabled


def _make_svg_icon(svg_data, color, disabled_color=None):
    return QIcon(_SvgIconEngine(svg_data, color, disabled_color))


def load_svg_icon(svg_path, color, disabled_color=None):
    """ Load an SVG and create a QIcon backed by `_SvgIconEngine` """
    with open(svg_path, "r") as f:
        svg_data = f.read()
    return _make_svg_icon(svg_data, color, disabled_color)


def _apply_icon(btn, svg_path, icon_info, default_size):
    """ Apply an SVG icon to a button, handling auto_resize """
    btn.setText("")
    color, disabled_color = get_icon_colors(btn)
    color = icon_info.get('color', color)
    disabled_color = icon_info.get('disabled_color', disabled_color)
    max_size = icon_info.get('size')

    with open(svg_path, "r") as f:
        svg_data = f.read()
    btn.setIcon(_make_svg_icon(svg_data, color, disabled_color))

    if icon_info.get('auto_resize'):
        side = min(btn.width(), btn.height())
        if max_size:
            side = min(side, max_size)
        btn.setIconSize(QSize(side, side))
        resizer = _ButtonIconResizer(btn, max_size)
        btn.installEventFilter(resizer)
        return

    btn.setStyleSheet("text-align: center; padding-left: 0;")
    size = icon_info.get('size', default_size)
    btn.setIconSize(QSize(size, size))


def set_switch_text(widget, btn_name, icons_dict, text_index):
    """ Switch button text to the element at text_index in the text list """
    icon_info = icons_dict.get(btn_name)
    if icon_info is None:
        return

    texts = icon_info.get('text')
    if not isinstance(texts, list):
        return

    btn = getattr(widget, btn_name, None)
    if btn is not None:
        btn.setText(texts[text_index])


def set_switch_icon(widget, btn_name, icons_dict, icons_path,
                    icon_index, default_size=16):
    """ Switch a button icon to the element at icon_index in the icon list """
    icon_info = icons_dict.get(btn_name)
    if icon_info is None:
        return

    icons = icon_info.get('icon')
    if not isinstance(icons, list):
        return

    icon_file = icons[icon_index]
    svg_path = os.path.join(icons_path, icon_file)
    btn = getattr(widget, btn_name, None)
    if btn is not None and os.path.exists(svg_path):
        _apply_icon(btn, svg_path, icon_info, default_size)


def set_active(btn, active):
    btn.setProperty("active", active)
    btn.style().unpolish(btn)
    btn.style().polish(btn)


def refresh_icon(widget, btn_name, icons_dict, icons_path, default_size=16):
    """ Refresh a non-list icon (re-reads palette colors) """
    icon_info = icons_dict.get(btn_name)
    if icon_info is None:
        return

    icon_value = icon_info.get('icon')
    if isinstance(icon_value, list):
        return

    svg_path = os.path.join(icons_path, icon_value)
    btn = getattr(widget, btn_name, None)
    if btn is not None and os.path.exists(svg_path):
        _apply_icon(btn, svg_path, icon_info, default_size)


def setup_icons(widget, icons_dict, icons_path,
                default_size=Const.ICON_DEFAULT_SIZE):
    """ Set up SVG icons on buttons defined in an icons dictionary """
    for btn_name, icon_info in icons_dict.items():
        btn = getattr(widget, btn_name, None)

        if btn is None:
            continue

        icon_value = icon_info.get('icon')
        svg_path = None

        if icon_value:
            icon_file = icon_value[0] if isinstance(
                icon_value, list) else icon_value

            svg_path = os.path.join(icons_path, icon_file)

            if not os.path.exists(svg_path):
                svg_path = None

        if svg_path is None:
            icon_text = icon_info.get('text')
            if icon_text:
                text = icon_text[0] if isinstance(
                    icon_text, list) else icon_text
                btn.setText(text)
            continue

        _apply_icon(btn, svg_path, icon_info, default_size)
