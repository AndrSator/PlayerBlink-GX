import sys

from PySide6.QtCore import QRectF, Qt, Property
from PySide6.QtGui import QPainter, QColor, QPainterPath
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, \
    QHBoxLayout, QSlider, QLabel, QPushButton, QColorDialog


class CProgressBar(QWidget):
    def __init__(self, total_segments=20, progress=5):
        super().__init__()
        self._total_segments = total_segments
        self._progress = progress
        self._gap_ratio = 0.8
        self._join_colors = False
        self._color_active = QColor("#00C853")
        self._color_inactive = QColor("#E0E0E0")
        self._color_label = QColor("#FFFFFF")

    @property
    def total_segments(self):
        return self._total_segments

    @total_segments.setter
    def total_segments(self, value):
        self._total_segments = value
        self.update()

    @property
    def gap_ratio(self):
        return self._gap_ratio

    @gap_ratio.setter
    def gap_ratio(self, value):
        self._gap_ratio = value
        self.update()

    @property
    def join_colors(self):
        return self._join_colors

    @join_colors.setter
    def join_colors(self, value):
        self._join_colors = value
        self.update()

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value
        self.update()

    @property
    def color_active(self):
        return self._color_active

    @color_active.setter
    def color_active(self, color):
        self._color_active = QColor(color)
        self.update()

    @property
    def color_inactive(self):
        return self._color_inactive

    @color_inactive.setter
    def color_inactive(self, color):
        self._color_inactive = QColor(color)
        self.update()

    @property
    def color_label(self):
        return self._color_label

    @color_label.setter
    def color_label(self, color):
        self._color_label = QColor(color)
        self.update()

    activeColor = Property(QColor, color_active.fget, color_active.fset)
    inactiveColor = Property(QColor, color_inactive.fget, color_inactive.fset)
    labelColor = Property(QColor, color_label.fget, color_label.fset)


class LinearProgress(CProgressBar):
    def __init__(self, total_segments=20, progress=5):
        super().__init__(total_segments, progress)
        self._gap_px = 2
        self.setMinimumHeight(10)

    @property
    def gap_px(self):
        return self._gap_px

    @gap_px.setter
    def gap_px(self, value):
        self._gap_px = max(0, int(value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        w, h = self.width(), self.height()
        n = self._total_segments
        half = self._gap_px // 2

        i = 0
        while i < n:
            color = self._color_active if i < self._progress \
                else self._color_inactive
            j = i + 1
            if self._join_colors:
                while j < n:
                    c = self._color_active if j < self._progress \
                        else self._color_inactive
                    if c != color:
                        break
                    j += 1

            x0 = round(i * w / n)
            x1 = round(j * w / n)
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawRect(x0 + half, 0, x1 - x0 - self._gap_px, h)
            i = j


class CircularProgress(CProgressBar):
    def __init__(self, total_segments=20, progress=5):
        super().__init__(total_segments, progress)
        self.thickness = 0.15  # 0.0-1.0, proportion of radius
        self.setMinimumSize(25, 25)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        size = min(self.width(), self.height())
        cx, cy = self.width() / 2.0, self.height() / 2.0
        outer_r = size / 2.0 - 5
        inner_r = max(outer_r * (1.0 - self.thickness), 1)

        gap_degrees = (1.0 - self._gap_ratio) * (360.0 / self._total_segments)
        seg_degrees = 360.0 / self._total_segments - gap_degrees

        outer_rect = QRectF(cx - outer_r, cy - outer_r,
                            outer_r * 2, outer_r * 2)
        inner_rect = QRectF(cx - inner_r, cy - inner_r,
                            inner_r * 2, inner_r * 2)

        painter.setPen(Qt.NoPen)

        # Group consecutive segments of the same color into single arcs
        step = 360.0 / self._total_segments
        i = 0
        while i < self._total_segments:
            color = self._color_active if i < self._progress \
                else self._color_inactive
            j = i + 1
            if self._join_colors:
                while j < self._total_segments:
                    c = self._color_active if j < self._progress \
                        else self._color_inactive
                    if c != color:
                        break
                    j += 1
            count = j - i

            painter.setBrush(color)

            group_start = 90.0 - i * step - gap_degrees / 2
            group_sweep = -(count * seg_degrees + (count - 1) * gap_degrees)

            path = QPainterPath()
            path.arcMoveTo(outer_rect, group_start)
            path.arcTo(outer_rect, group_start, group_sweep)
            path.arcTo(inner_rect, group_start + group_sweep, -group_sweep)
            path.closeSubpath()

            painter.drawPath(path)
            i = j

        # Show progress text
        if self._progress > 0:
            font = painter.font()
            font.setPixelSize(max(int(inner_r * 0.6), 10))
            painter.setFont(font)
            painter.setPen(self._color_label)
            painter.drawText(QRectF(cx - inner_r, cy - inner_r,
                                    inner_r * 2, inner_r * 2),
                             Qt.AlignCenter, str(self._progress))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("CircularProgress Playground")
    window.resize(500, 200)

    v_layout = QVBoxLayout(window)
    layout = QHBoxLayout()

    v_layout.addLayout(layout, stretch=1)

    # Linear Progress bar
    lpb = LinearProgress(total_segments=20, progress=5)
    v_layout.addWidget(lpb, stretch=1)

    # Circular Progress bar
    cpb = CircularProgress(total_segments=20, progress=5)
    layout.addWidget(cpb, stretch=1)

    # Controls panel
    controls = QVBoxLayout()
    layout.addLayout(controls)

    def make_slider(label, min_val, max_val, initial, callback):
        row = QHBoxLayout()
        lbl = QLabel(f"{label}: {initial}")
        lbl.setFixedWidth(140)
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(initial)

        def on_change(v):
            lbl.setText(f"{label}: {v}")
            callback(v)

        slider.valueChanged.connect(on_change)
        row.addWidget(lbl)
        row.addWidget(slider)
        controls.addLayout(row)
        return slider

    def make_float_slider(label, min_val, max_val, initial, callback):
        row = QHBoxLayout()
        lbl = QLabel(f"{label}: {initial:.2f}")
        lbl.setFixedWidth(140)
        slider = QSlider(Qt.Horizontal)
        slider.setRange(int(min_val * 100), int(max_val * 100))
        slider.setValue(int(initial * 100))

        def on_change(v):
            fv = v / 100.0
            lbl.setText(f"{label}: {fv:.2f}")
            callback(fv)

        slider.valueChanged.connect(on_change)
        row.addWidget(lbl)
        row.addWidget(slider)
        controls.addLayout(row)
        return slider

    def set_segments(v):
        for w in (cpb, lpb):
            w.total_segments = v
            w.progress = min(w.progress, v)
        progress_slider.setMaximum(v)

    def set_progress(v):
        for w in (cpb, lpb):
            w.progress = min(v, w.total_segments)

    def set_thickness(v):
        cpb.thickness = v
        cpb.update()

    def set_gap(v):
        for w in (cpb, lpb):
            w.gap_ratio = v

    make_slider("Segments", 2, 60, 20, set_segments)
    progress_slider = make_slider("Progress", 0, 20, 5, set_progress)
    make_float_slider("Thickness", 0.05, 1.00, 0.15, set_thickness)
    make_float_slider("Gap ratio", 0.10, 1.00, 0.80, set_gap)

    from PySide6.QtWidgets import QCheckBox
    chk_join = QCheckBox("Join colors")
    chk_join.setChecked(False)

    def set_join(state):
        for w in (cpb, lpb):
            w.join_colors = bool(state)
            w.update()

    chk_join.stateChanged.connect(set_join)
    controls.addWidget(chk_join)

    def pick_active_color():
        color = QColorDialog.getColor(
            cpb.color_active, window, "Active color")
        if color.isValid():
            for w in (cpb, lpb):
                w.color_active = color

    def pick_inactive_color():
        color = QColorDialog.getColor(
            cpb.color_inactive, window, "Inactive color")
        if color.isValid():
            for w in (cpb, lpb):
                w.color_inactive = color

    btn_active = QPushButton("Active color")
    btn_active.clicked.connect(pick_active_color)
    controls.addWidget(btn_active)

    btn_inactive = QPushButton("Inactive color")
    btn_inactive.clicked.connect(pick_inactive_color)
    controls.addWidget(btn_inactive)

    def pick_label_color():
        color = QColorDialog.getColor(
            cpb.color_label, window, "Label color")
        if color.isValid():
            for w in (cpb, lpb):
                w.color_label = color

    btn_label = QPushButton("Label color")
    btn_label.clicked.connect(pick_label_color)
    controls.addWidget(btn_label)

    controls.addStretch()

    window.show()
    sys.exit(app.exec())
