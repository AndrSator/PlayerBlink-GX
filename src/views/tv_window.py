import cv2

from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QRubberBand
from PySide6.QtGui import QImage
from PySide6.QtCore import Qt, QSize, QRect, QPoint, Signal

from .cwindow import CWindow
from ..widgets.gl_display import GLDisplay
from .icon_utils import setup_icons, set_switch_icon, refresh_icon
from ..log import logger
from ..constants import Constants as Const
from ..preferences import Preferences as Prefs

from ..ui.tv_ui import Ui_tv_view


ICONS = {
    "switch_capture": {
        "icon": ["videocam.svg", "videocam_off.svg"],
        "tooltip_id": ["start_capture", "stop_capture"],
    },
    "switch_pause": {
        "icon": ["resume.svg", "pause.svg"],
        "tooltip_id": ["resume_capture", "pause_capture"],
    },
    "switch_crop_tracking_area": {
        "icon": ["pageless.svg", "screenshot_region.svg"],
        "tooltip_id": ["activate_crop_mode", "deactivate_crop_mode"],
    },
    "switch_crop_eye": {
        "icon": ["eye_tracking.svg", "screenshot_region.svg"],
        "tooltip_id": ["activate_crop_mode", "deactivate_crop_mode"],
    },
    "btn_device_prev": {
        "icon": "arrow_left.svg",
        "tooltip_id": "previous_device",
    },
    "btn_device_next": {
        "icon": "arrow_right.svg",
        "tooltip_id": "next_device",
    },
    "btn_adjust_screen": {
        "icon": "fit_screen.svg",
        "tooltip_id": "adjust_screen",
    },
    "switch_monitor_mode": {
        "icon": ["desktop_landscape.svg", "cable.svg"],
        "tooltip_id": ["monitor_mode_on", "monitor_mode_off"],
    },
}


_ROI_CORNER_GRAB_PX = 12  # px tolerance for corner resize handles
_ROI_EDGE_GRAB_PX = 6     # px tolerance for interior move detection

# BGR888 format skips cv2.cvtColor entirely (available since Qt 5.14)
_BGR888 = getattr(QImage, "Format_BGR888", None)


class TvWindow(CWindow):
    # Signals emitted to the Controller
    crop_started = Signal()
    crop_finished = Signal()
    eye_cropped = Signal(object)  # cropped numpy array
    # x, y, w, h in frame coords
    tracking_area_defined = Signal(int, int, int, int)

    def __init__(self):
        super().__init__()
        self._tv_ui = Ui_tv_view()
        self._tv_ui.setupUi(self.placeholder_content)

        if not self.placeholder_content.layout():
            QVBoxLayout(self.placeholder_content)

        self._tracking = False
        self._last_frame = None

        # Replace QOpenGLWidget with custom GLDisplay
        prefs = Prefs()
        old_display = self._tv_ui.display
        gl_display = GLDisplay(
            old_display.parentWidget(),
            gpu_scaling=prefs.gpu_rendering,
            smooth=prefs.smooth_scaling,
        )
        self._tv_ui.verticalLayout_6.replaceWidget(old_display, gl_display)
        old_display.deleteLater()
        self._tv_ui.display = gl_display

        self.display.setSizePolicy(
            QSizePolicy.Policy.Ignored,
            QSizePolicy.Policy.Ignored,
        )

        # Crop mode: None, "eye", or "tracking_area"
        self._crop_mode = None
        self._crop_origin = QPoint()
        self._rubber_band = QRubberBand(QRubberBand.Rectangle, self.display)

        # Tracking area in frame coordinates
        self._tracking_area = None

        # Eye match overlay (from EyeTracker): (x, y, w, h) in frame coords
        self._eye_match = None

        # Monitor mode state
        self._monitor_mode = False

        # ROI drag/resize state
        self._roi_drag_mode = None    # "move", "tl", "tr", "bl", "br"
        self._roi_drag_origin = None
        self._roi_drag_start = None

        self.display.setMouseTracking(True)
        self.display.installEventFilter(self)

        self.update_buttons_visibility()

    # region Properties

    @property
    def display(self):
        return self._tv_ui.display

    @property
    def btn_device_prev(self):
        return self._tv_ui.btn_device_prev

    @property
    def btn_device_next(self):
        return self._tv_ui.btn_device_next

    @property
    def btn_device_refresh(self):
        return self._tv_ui.btn_device_refresh

    @property
    def cmb_windows_list(self):
        return self._tv_ui.cmb_windows_list

    @property
    def btn_adjust_screen(self):
        return self._tv_ui.btn_adjust_screen

    @property
    def switch_capture(self):
        return self._tv_ui.switch_capture

    @property
    def switch_pause(self):
        return self._tv_ui.switch_pause

    @property
    def switch_crop_tracking_area(self):
        return self._tv_ui.switch_crop_tracking_area

    @property
    def switch_crop_eye(self):
        return self._tv_ui.switch_crop_eye

    @property
    def switch_monitor_mode(self):
        return self._tv_ui.switch_monitor_mode

    @property
    def tracking(self):
        return self._tracking

    @tracking.setter
    def tracking(self, value):
        self._tracking = value

    # endregion

    def set_eye_match(self, match_rect):
        """Set the eye match rectangle (x, y, w, h) or None to clear."""
        self._eye_match = match_rect
        self.display.set_eye_match(match_rect)
        self.display.update()

    def toggle_crop_eye(self):
        self._toggle_crop_mode("eye")

    def toggle_crop_tracking_area(self):
        self._toggle_crop_mode("tracking_area")

    def _toggle_crop_mode(self, mode):
        if self._crop_mode == mode:
            # Deactivate
            logger.debug(f"Crop mode deactivated: {mode}")
            self._crop_mode = None
        elif self._crop_mode is not None:
            # Switch from one mode to another - deactivate current first
            logger.debug(f"Crop mode switched: {self._crop_mode} -> {mode}")
            self._update_crop_button(self._crop_mode, False)
            self._crop_mode = mode
        else:
            logger.debug(f"Crop mode activated: {mode}")
            self._crop_mode = mode

        active = self._crop_mode == mode
        self._update_crop_button(mode, active)

        if self._crop_mode is None:
            self._rubber_band.hide()
            self.display.setCursor(Qt.ArrowCursor)

    def _update_crop_button(self, mode, active):
        btn_name = "switch_crop_eye" if mode == "eye" \
            else "switch_crop_tracking_area"
        btn = getattr(self, btn_name)
        self._set_active(btn, active)
        self._set_switch_icon(btn_name, 1 if active else 0)

    def set_monitor_mode(self, enabled):
        self._monitor_mode = enabled
        self._set_switch_icon(
            "switch_monitor_mode",
            1 if self._monitor_mode else 0)
        self.update_buttons_visibility()

    def populate_window_menu(self, windows):
        self.cmb_windows_list.clear()
        for title in windows:
            self.cmb_windows_list.addItem(title)
            logger.debug(f"[TvWindow] Added window to menu: {title}")

    def patch_single_item_combo(self):
        """ Patch the window combo so that with a single item
        (Linux portal placeholder)"""
        combo = self.cmb_windows_list
        original_show_popup = combo.showPopup

        def patched_show_popup():
            if combo.count() == 1:
                combo.activated.emit(0)
                return
            original_show_popup()

        combo.showPopup = patched_show_popup

    def clear_display(self):
        self._last_frame = None
        self.display.clear()

    def set_error_text(self):
        self.display.setText("ERROR: Unable to start capture")

    def set_minimized_text(self):
        self._last_frame = None
        self.display.setText("Window is minimized")

    def clear_error_text(self):
        self.display.setText("")

    def set_device_name(self, name):
        self.btn_device_refresh.setText(name)

    def set_no_input(self):
        self.btn_device_refresh.setText("NO INPUT FOUND")
        self.set_devices_controls(False)

    def set_no_windows_text(self):
        self._last_frame = None
        self.display.setText("No windows found")

    def set_devices_controls(self, enabled=True):
        self.btn_device_prev.setEnabled(enabled)
        self.btn_device_next.setEnabled(enabled)

    def set_monitor_controls(self, enabled=True):
        self.switch_monitor_mode.setEnabled(enabled)

    def set_devices_controls_visibility(self, visible=True):
        self.btn_device_prev.setVisible(visible)
        self.btn_device_next.setVisible(visible)
        self.btn_device_refresh.setVisible(visible)
        self.cmb_windows_list.setVisible(not visible)

    def update_switch_icons(self, capturing, paused):
        self._set_active(self.switch_pause, paused)

        self._set_switch_icon("switch_capture", 0 if capturing else 1)
        self._set_switch_icon("switch_pause", 0 if paused else 1)
        self._set_switch_icon("switch_crop_tracking_area",
                              1 if self._crop_mode == "tracking_area" else 0)
        self._set_switch_icon("switch_crop_eye",
                              1 if self._crop_mode == "eye" else 0)
        self._refresh_icon("btn_adjust_screen")

        self.switch_pause.setEnabled(capturing)
        self.switch_crop_tracking_area.setEnabled(capturing)
        # switch_crop_eye enabled state is managed by the Controller
        self.btn_adjust_screen.setEnabled(capturing)

    def apply_tracking_area(self, x, y, w, h):
        """Set tracking area visually without emitting signal."""
        self._tracking_area = (x, y, w, h)
        self.display.set_tracking_area((x, y, w, h))
        self.display.update()

    def _set_tracking_area(self, x, y, w, h):
        self.apply_tracking_area(x, y, w, h)
        self.tracking_area_defined.emit(x, y, w, h)

    def push_frame(self, frame):
        """Receive a frame from the Controller and display it.

        Pipeline (GPU mode):
          frame (BGR numpy) → QImage(Format_BGR888).copy() → GLDisplay
          GPU scales via texture sampling. No cvtColor, no QPixmap,
          no CPU scaling. One memory copy instead of three.
        """
        # Skip if same frame object (timer fired faster than capture)
        if self._last_frame is frame:
            return

        first = self._last_frame is None
        self._last_frame = frame

        h, w = frame.shape[:2]

        if _BGR888 is not None:
            # Direct BGR → QImage, no cv2.cvtColor needed
            qimage = QImage(
                frame.data, w, h, frame.strides[0], _BGR888).copy()
        else:
            # Fallback: convert BGR → RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            qimage = QImage(
                rgb.data, w, h, rgb.strides[0],
                QImage.Format_RGB888).copy()

        self.display.set_frame(qimage, raw_frame=frame.copy())

        if first:
            self.adjust_screen()

    def eventFilter(self, obj, event):
        if obj is not self.display:
            return super().eventFilter(obj, event)

        etype = event.type()

        # Crop mode (original behaviour)
        if self._crop_mode is not None:
            return self._handle_crop_event(etype, event)

        #  ROI drag/resize (allowed when crop_tracking_area button is enabled)
        if self._tracking_area is not None \
                and self.switch_crop_tracking_area.isEnabled():
            handled = self._handle_roi_event(etype, event)
            if handled:
                return True

        return super().eventFilter(obj, event)

    # region ROI

    def _get_display_metrics(self):
        """Return (offset_x, offset_y, px_w, px_h, scale_x, scale_y)
        for converting between widget and frame coordinate spaces.
        Returns None if no frame is available."""
        if self._last_frame is None:
            return None

        cr = self.display.content_rect()
        if cr.isEmpty():
            return None

        px_w, px_h = cr.width(), cr.height()
        offset_x = cr.x()
        offset_y = cr.y()

        frame_h, frame_w = self._last_frame.shape[:2]
        sx = frame_w / px_w
        sy = frame_h / px_h
        return offset_x, offset_y, px_w, px_h, sx, sy

    def _tracking_area_label_rect(self):
        """Return the tracking area as a QRect in widget coordinates,
        or None if unavailable."""
        if self._tracking_area is None:
            return None
        m = self._get_display_metrics()
        if m is None:
            return None

        off_x, off_y, _pw, _ph, sx, sy = m
        x, y, w, h = self._tracking_area
        rx = int(x / sx) + off_x
        ry = int(y / sy) + off_y
        rw = int(w / sx)
        rh = int(h / sy)
        return QRect(rx, ry, rw, rh)

    def _roi_hit_test(self, pos):
        """ Determine what part of the ROI the cursor is on """
        r = self._tracking_area_label_rect()
        if r is None:
            return None

        px, py = pos.x(), pos.y()
        g = _ROI_CORNER_GRAB_PX

        corners = {
            "tl": QPoint(r.left(), r.top()),
            "tr": QPoint(r.right(), r.top()),
            "bl": QPoint(r.left(), r.bottom()),
            "br": QPoint(r.right(), r.bottom()),
        }
        for name, cp in corners.items():
            if abs(px - cp.x()) <= g and abs(py - cp.y()) <= g:
                return name

        if r.adjusted(
            -_ROI_EDGE_GRAB_PX, -_ROI_EDGE_GRAB_PX,
                _ROI_EDGE_GRAB_PX, _ROI_EDGE_GRAB_PX).contains(pos):
            return "move"

        return None

    _CORNER_CURSORS = {
        "tl": Qt.SizeFDiagCursor,
        "tr": Qt.SizeBDiagCursor,
        "bl": Qt.SizeBDiagCursor,
        "br": Qt.SizeFDiagCursor,
        "move": Qt.SizeAllCursor,
    }

    def _handle_roi_event(self, etype, event):
        """ Handle mouse events for dragging / resizing the ROI """

        if etype == event.Type.MouseMove and self._roi_drag_mode is None:
            # Hover: update cursor based on hit zone
            hit = self._roi_hit_test(event.pos())
            cursor = self._CORNER_CURSORS.get(hit)
            self.display.setCursor(cursor if cursor else Qt.ArrowCursor)
            return False  # don't consume, just update cursor

        if etype == event.Type.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                hit = self._roi_hit_test(event.pos())
                if hit:
                    self._roi_drag_mode = hit
                    self._roi_drag_origin = event.pos()
                    self._roi_drag_start = self._tracking_area
                    return True

        if etype == event.Type.MouseMove and self._roi_drag_mode is not None:
            if event.buttons() & Qt.LeftButton:
                self._apply_roi_drag(event.pos())
                return True

        if etype == event.Type.MouseButtonRelease:
            if self._roi_drag_mode is not None:
                self._apply_roi_drag(event.pos())
                self._roi_drag_mode = None
                self._roi_drag_origin = None
                self._roi_drag_start = None

                x, y, w, h = self._tracking_area
                self._set_tracking_area(x, y, w, h)
                return True

        if etype == event.Type.Leave:
            if self._roi_drag_mode is None:
                self.display.setCursor(Qt.ArrowCursor)

        return False

    def _apply_roi_drag(self, pos):
        """ Apply the drag delta to the ROI, converting label-space
        movement to frame-space coordinates """

        m = self._get_display_metrics()
        if m is None or self._roi_drag_start is None:
            return

        _off_x, _off_y, _pw, _ph, sx, sy = m
        dx_label = pos.x() - self._roi_drag_origin.x()
        dy_label = pos.y() - self._roi_drag_origin.y()
        dx_frame = int(dx_label * sx)
        dy_frame = int(dy_label * sy)

        ox, oy, ow, oh = self._roi_drag_start
        frame_h, frame_w = self._last_frame.shape[:2]

        if self._roi_drag_mode == "move":
            nx = max(0, min(ox + dx_frame, frame_w - ow))
            ny = max(0, min(oy + dy_frame, frame_h - oh))
            self._set_tracking_area(nx, ny, ow, oh)

        else:
            # Corner resize
            x1, y1 = ox, oy
            x2, y2 = ox + ow, oy + oh
            min_size = 10  # minimum ROI dimension in frame pixels

            mode = self._roi_drag_mode
            if "l" in mode:
                x1 = max(0, min(ox + dx_frame, x2 - min_size))
            if "r" in mode:
                x2 = max(x1 + min_size, min(ox + ow + dx_frame, frame_w))
            if "t" in mode:
                y1 = max(0, min(oy + dy_frame, y2 - min_size))
            if "b" in mode:
                y2 = max(y1 + min_size, min(oy + oh + dy_frame, frame_h))

            self._set_tracking_area(x1, y1, x2 - x1, y2 - y1)

    # endregion

    # region Crop

    def _handle_crop_event(self, etype, event):
        if etype == event.Type.Enter:
            self.display.setCursor(Qt.CrossCursor)
            return True

        if etype == event.Type.Leave:
            self.display.setCursor(Qt.ArrowCursor)
            return True

        if etype == event.Type.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.crop_started.emit()
                self._crop_origin = event.pos()
                self._rubber_band.setGeometry(
                    QRect(self._crop_origin, QSize()))
                self._rubber_band.show()
                return True

        if etype == event.Type.MouseMove:
            if event.buttons() & Qt.LeftButton:
                self._rubber_band.setGeometry(
                    QRect(self._crop_origin, event.pos()).normalized())
                return True

        if etype == event.Type.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                self._rubber_band.hide()
                rect = QRect(
                    self._crop_origin, event.pos()).normalized()
                frame_rect = self._label_rect_to_frame(rect)

                if frame_rect and self._crop_mode == "eye":
                    cropped = self._extract_crop(frame_rect)
                    if cropped is not None:
                        self.eye_cropped.emit(cropped)
                elif frame_rect and self._crop_mode == "tracking_area":
                    x, y, w, h = frame_rect
                    self._set_tracking_area(x, y, w, h)

                current_mode = self._crop_mode
                self.crop_finished.emit()
                self._toggle_crop_mode(current_mode)  # deactivate
                return True

        return super().eventFilter(self.display, event)

    # endregion

    def _label_rect_to_frame(self, rect):
        """Convert a QRect in widget coordinates to (x, y, w, h)
        in frame coordinates."""
        if rect.isEmpty() or self._last_frame is None:
            return None

        cr = self.display.content_rect()
        if cr.isEmpty():
            return None

        frame_h, frame_w = self._last_frame.shape[:2]
        px_w, px_h = cr.width(), cr.height()
        offset_x = cr.x()
        offset_y = cr.y()

        local_x = max(0, rect.x() - offset_x)
        local_y = max(0, rect.y() - offset_y)
        local_w = min(rect.width(), px_w - local_x)
        local_h = min(rect.height(), px_h - local_y)

        if local_w <= 0 or local_h <= 0:
            return None

        scale_x = frame_w / px_w
        scale_y = frame_h / px_h

        x = max(0, min(int(local_x * scale_x), frame_w - 1))
        y = max(0, min(int(local_y * scale_y), frame_h - 1))
        w = min(int(local_w * scale_x), frame_w - x)
        h = min(int(local_h * scale_y), frame_h - y)

        if w <= 0 or h <= 0:
            return None

        return (x, y, w, h)

    def _extract_crop(self, frame_rect):
        """Extract a region of the last frame as a numpy array."""
        x, y, w, h = frame_rect
        cropped = self._last_frame[y:y + h, x:x + w]
        if cropped.size == 0:
            return None
        return cropped.copy()

    def adjust_screen(self):
        video_w, video_h = self.display.frame_size()
        if video_w <= 0 or video_h <= 0:
            return

        video_ratio = video_w / video_h

        label_w = self.display.width()
        label_h = self.display.height()

        fitted_w = label_w
        fitted_h = round(label_w / video_ratio)
        if fitted_h > label_h:
            fitted_h = label_h
            fitted_w = round(label_h * video_ratio)

        dw = label_w - fitted_w
        dh = label_h - fitted_h
        self.resize(self.width() - dw, self.height() - dh)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # GLDisplay handles its own repaint on resize via paintGL

    def _set_active(self, btn, active):
        btn.setProperty("active", active)
        btn.style().unpolish(btn)
        btn.style().polish(btn)

    def _refresh_icon(self, btn_name):
        refresh_icon(self, btn_name, ICONS, Const.ICONS_DIR,
                     Const.ICON_DEFAULT_SIZE)

    def _set_switch_icon(self, btn_name, icon_index):
        set_switch_icon(self, btn_name, ICONS, Const.ICONS_DIR,
                        icon_index, Const.ICON_DEFAULT_SIZE)

    def _setup_icons(self):
        super()._setup_icons()
        setup_icons(self, ICONS, Const.ICONS_DIR, Const.ICON_DEFAULT_SIZE)

    def update_buttons_visibility(self):
        self.set_devices_controls_visibility(not self._monitor_mode)
