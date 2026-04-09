import cv2

from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QImage, QPainter, QPen, QColor
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from ..log import logger

# Cache Format_BGR888 availability (PySide6 >= 6.2)
_BGR888 = getattr(QImage.Format, "Format_BGR888", None)


class GLDisplay(QOpenGLWidget):
    """ GPU-accelerated video display widget.

    Renders frames as OpenGL textures via QPainter on QOpenGLWidget.
    Uses INTER_AREA pre-scaling for sharp downscaling.

    """

    def __init__(self, parent=None, gpu_scaling=True, smooth=True):
        super().__init__(parent)
        self._qimage = None
        self._scaled_qimage = None  # pre-scaled for downscaling
        self._text = None
        self._frame_w = 0
        self._frame_h = 0
        self._content_rect = QRect()
        self._last_scaled_size = QSize()

        # Overlay data (in frame coordinates)
        self._tracking_area = None
        self._eye_match = None

        # Rendering config
        self._gpu_scaling = gpu_scaling
        self._smooth = smooth

    # region General API

    def set_frame(self, qimage: QImage, raw_frame=None):
        """ Set the current frame to display. Triggers a GPU repaint.

        Args:
            qimage: QImage for fallback/upscaling rendering.
            raw_frame: Optional numpy BGR array for sharp INTER_AREA
                       downscaling.
        """
        first = self._qimage is None
        self._qimage = qimage
        self._frame_w = qimage.width()
        self._frame_h = qimage.height()
        self._text = None

        # Pre-scale for downscaling: INTER_AREA on CPU, then 1:1 blit
        self._scaled_qimage = None
        cr = self._content_rect
        if (raw_frame is not None and self._gpu_scaling
                and not cr.isEmpty()
                and (cr.width() < self._frame_w
                     or cr.height() < self._frame_h)):
            dpr = self.devicePixelRatio()
            phys_w = round(cr.width() * dpr)
            phys_h = round(cr.height() * dpr)
            self._prescale(raw_frame, phys_w, phys_h, dpr)

        self.update()

        if first:
            logger.debug(
                f"[GLDisplay] First frame received: "
                f"{self._frame_w}x{self._frame_h} "
                f"format={qimage.format().name} "
                f"depth={qimage.depth()}bit")

    def set_tracking_area(self, area):
        self._tracking_area = area

    def set_eye_match(self, match):
        self._eye_match = match

    def set_smooth(self, smooth: bool):
        self._smooth = smooth

    def set_gpu_scaling(self, enabled: bool):
        self._gpu_scaling = enabled

    def content_rect(self) -> QRect:
        return QRect(self._content_rect)

    def frame_size(self) -> tuple[int, int]:
        return self._frame_w, self._frame_h

    def clear(self):
        self._qimage = None
        self._scaled_qimage = None
        self._text = None
        self.update()

    def setText(self, text: str):
        self._qimage = None
        self._text = text
        self.update()

    # endregion

    # region OpenGL rendering

    def initializeGL(self):
        ctx = self.context()
        if not ctx or not ctx.isValid():
            logger.warning("[GLDisplay] OpenGL context not available")
            return

        fmt = ctx.format()
        gl_info = (
            f"  OpenGL version:  {fmt.majorVersion()}.{fmt.minorVersion()}\n"
            f"  Profile:         {fmt.profile().name}\n"
            f"  Swap interval:   {fmt.swapInterval()} "
            f"({'vsync ON' if fmt.swapInterval() > 0 else 'vsync OFF'})\n"
            f"  Swap behavior:   {fmt.swapBehavior().name}\n"
            f"  GPU scaling:     {self._gpu_scaling}\n"
            f"  Smooth filter:   {self._smooth}")
        logger.debug(f"[GLDisplay] OpenGL initialized:\n{gl_info}")

    def resizeGL(self, _w, _h):
        self._recompute_content_rect()

    def paintGL(self):
        self._recompute_content_rect()

        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(22, 20, 22))

        if self._qimage is not None and not self._content_rect.isEmpty():
            cr = self._content_rect

            if self._scaled_qimage is not None:
                # Draw pre-scaled image 1:1 (sharp downscale)
                painter.drawImage(cr, self._scaled_qimage)
            elif self._gpu_scaling:
                # GPU bilinear (fine for 1:1 or upscaling)
                if self._smooth:
                    painter.setRenderHint(
                        QPainter.SmoothPixmapTransform)
                painter.drawImage(cr, self._qimage)
            else:
                # CPU fallback
                mode = Qt.SmoothTransformation if self._smooth \
                    else Qt.FastTransformation
                scaled = self._qimage.scaled(
                    cr.size(), Qt.IgnoreAspectRatio, mode)
                painter.drawImage(cr, scaled)

            # Overlays (drawn on top of the frame by the GPU)
            if self._tracking_area is not None:
                self._paint_tracking_area(painter)

            if self._eye_match is not None:
                self._paint_eye_match(painter)

        elif self._text:
            painter.setPen(QColor(200, 200, 200))
            painter.drawText(self.rect(), Qt.AlignCenter, self._text)

        painter.end()

    # endregion

    def _recompute_content_rect(self):
        if self._frame_w <= 0 or self._frame_h <= 0:
            self._content_rect = QRect()
            return

        ww, wh = self.width(), self.height()
        src_aspect = self._frame_w / self._frame_h

        fit_w = ww
        fit_h = round(ww / src_aspect)
        if fit_h > wh:
            fit_h = wh
            fit_w = round(wh * src_aspect)

        x = (ww - fit_w) // 2
        y = (wh - fit_h) // 2
        self._content_rect = QRect(x, y, fit_w, fit_h)

    def _prescale(self, bgr_frame, phys_w, phys_h, dpr):
        """Pre-scale a BGR frame with INTER_AREA at physical resolution."""
        scaled = cv2.resize(
            bgr_frame, (phys_w, phys_h),
            interpolation=cv2.INTER_AREA)
        h, w = scaled.shape[:2]

        if _BGR888 is not None:
            qimg = QImage(
                scaled.data, w, h, scaled.strides[0], _BGR888).copy()
        else:
            rgb = cv2.cvtColor(scaled, cv2.COLOR_BGR2RGB)
            qimg = QImage(
                rgb.data, w, h, rgb.strides[0],
                QImage.Format_RGB888).copy()

        # Mark as high-DPI so QPainter draws 1:1 to physical pixels
        qimg.setDevicePixelRatio(dpr)
        self._scaled_qimage = qimg
        self._last_scaled_size = QSize(phys_w, phys_h)

    def _paint_tracking_area(self, painter):
        cr = self._content_rect
        sx = cr.width() / self._frame_w
        sy = cr.height() / self._frame_h

        x, y, w, h = self._tracking_area
        rx = cr.x() + int(x * sx)
        ry = cr.y() + int(y * sy)
        rw = int(w * sx)
        rh = int(h * sy)
        corner = min(rw, rh) // 4

        pen = QPen(QColor(255, 0, 0), 2)
        painter.setPen(pen)
        for cx, cy, dx, dy in [
            (rx, ry, 1, 1),
            (rx + rw, ry, -1, 1),
            (rx, ry + rh, 1, -1),
            (rx + rw, ry + rh, -1, -1),
        ]:
            painter.drawLine(cx, cy, cx + corner * dx, cy)
            painter.drawLine(cx, cy, cx, cy + corner * dy)

    def _paint_eye_match(self, painter):
        cr = self._content_rect
        sx = cr.width() / self._frame_w
        sy = cr.height() / self._frame_h

        mx, my, mw, mh = self._eye_match
        emx = cr.x() + int(mx * sx)
        emy = cr.y() + int(my * sy)
        emw = int(mw * sx)
        emh = int(mh * sy)

        pen = QPen(QColor(0, 120, 255), 2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(emx, emy, emw, emh)
