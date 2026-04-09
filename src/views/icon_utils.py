import os

from PySide6.QtGui import QIcon, QPainter, QPixmap, QPalette
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import Qt, QByteArray, QObject, QEvent, QSize

from ..constants import Constants as Const

__version__ = "1.0.0"


# Default fill used by Google Material SVG icons
_DEFAULT_SVG_FILL = 'fill="#e3e3e3"'


class _ButtonIconResizer(QObject):
    """ Re-renders SVG icons at the button size on resize """

    def __init__(self, btn, svg_data, color, disabled_color, max_size=None):
        super().__init__(btn)
        self._svg_data = svg_data
        self._color = color
        self._disabled_color = disabled_color
        self._max_size = max_size

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Resize:
            side = min(obj.width(), obj.height())
            if self._max_size:
                side = min(side, self._max_size)
            size = QSize(side, side)
            obj.setIconSize(size)
            icon = QIcon()
            icon.addPixmap(
                _render_svg(self._svg_data, self._color, size),
                QIcon.Normal)
            if self._disabled_color:
                icon.addPixmap(
                    _render_svg(self._svg_data, self._disabled_color, size),
                    QIcon.Disabled)
            obj.setIcon(icon)
        return False


def _render_svg(svg_data, color, size=None):
    """ Render SVG string data to a QPixmap with the given fill color """
    colored = svg_data.replace(_DEFAULT_SVG_FILL, f'fill="{color}"')
    renderer = QSvgRenderer(QByteArray(colored.encode()))
    target_size = QSize(size) if size else renderer.defaultSize()
    pixmap = QPixmap(target_size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap


def get_icon_colors(btn):
    role = btn.foregroundRole()
    palette = btn.palette()
    normal = palette.color(QPalette.ColorGroup.Normal, role).name()
    disabled = palette.color(QPalette.ColorGroup.Disabled, role).name()
    return normal, disabled


def load_svg_icon(svg_path, color, disabled_color=None, size=None):
    """ Load an SVG and create a QIcon with Normal and Disabled modes """
    with open(svg_path, "r") as f:
        svg_data = f.read()

    icon = QIcon()
    icon.addPixmap(_render_svg(svg_data, color, size), QIcon.Normal)

    if disabled_color:
        icon.addPixmap(
            _render_svg(svg_data, disabled_color, size), QIcon.Disabled)

    return icon


def _apply_icon(btn, svg_path, icon_info, default_size):
    """ Apply an SVG icon to a button, handling auto_resize """
    btn.setText("")
    color, disabled_color = get_icon_colors(btn)
    color = icon_info.get('color', color)
    disabled_color = icon_info.get('disabled_color', disabled_color)
    max_size = icon_info.get('size')

    if icon_info.get('auto_resize'):
        with open(svg_path, "r") as f:
            svg_data = f.read()
        side = min(btn.width(), btn.height())
        if max_size:
            side = min(side, max_size)
        render_size = QSize(side, side)
        icon = QIcon()
        icon.addPixmap(
            _render_svg(svg_data, color, render_size), QIcon.Normal)
        if disabled_color:
            icon.addPixmap(
                _render_svg(svg_data, disabled_color, render_size),
                QIcon.Disabled)
        btn.setIcon(icon)
        btn.setIconSize(render_size)
        resizer = _ButtonIconResizer(
            btn, svg_data, color, disabled_color, max_size)
        btn.installEventFilter(resizer)
        return

    btn.setIcon(load_svg_icon(svg_path, color, disabled_color))
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
