from enum import Enum

from PySide6.QtWidgets import QSizePolicy, QGraphicsScene
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QEvent
from PySide6.QtGui import QPixmap

from ..utils import Utils
from ..eye_tracker import BlinkType
from ..constants import Constants as Const

from ..widgets.cadvance_label import AdvanceLabel
from ..widgets.cprogress import LinearProgress, CircularProgress
from ..widgets.cgallery import GalleryContainer

from .cwindow import CWindow
from .icon_utils import setup_icons, set_switch_icon
from ..ui.menu_ui import Ui_menu_view


_TABS = {
    "MAIN": 0,
    "EYE_MANAGER": 1,
    "CONFIGS": 2,
    "PREFERENCES": 3,
    "DEBUG": 4
}

_ICONS = {
    # Tabs
    "btn_eye_manager": {
        "icon": "folder_eye.svg",
    },
    "btn_configs": {
        "icon": "library_books.svg",
    },
    "btn_preferences": {
        "icon": "settings.svg",
    },
    "btn_debug": {
        "icon": "bug.svg",
    },
    # Other buttons
    "switch_tracking": {
        "icon": ["mystery.svg", "cancel.svg"],
        "size": Const.ICON_DEFAULT_SIZE_BIG
    },
    "switch_tracking_tidsid": {
        "icon": "id_card.svg",
        "size": Const.ICON_DEFAULT_SIZE_BIG
    },
    "btn_reidentify": {
        "icon": "sync.svg",
        "size": Const.ICON_DEFAULT_SIZE_BIG
    },
    "btn_start_countdown": {
        "icon": "timer.svg",
        "size": Const.ICON_DEFAULT_SIZE_BIG
    },
    "switch_seed_display": {
        "icon": "memory.svg",
        "size": Const.ICON_DEFAULT_SIZE_SMALL
    },
    "btn_create_resource": {
        "icon": "add_photo.svg",
    },
    "btn_delete_resource": {
        "icon": "delete.svg",
    },
    "btn_stop_timeline": {
        "icon": "stop.svg",
        "size": Const.ICON_DEFAULT_SIZE_SMALL
    },
    "btn_copy_timeline_adv": {
        "icon": "copy.svg",
        "size": Const.ICON_DEFAULT_SIZE_SMALL
    },
    # Config tab
    "btn_save_config": {
        "icon": "save.svg",
    },
    "btn_create_config": {
        "icon": "add.svg",
    },
    "btn_load_config": {
        "icon": "check.svg",
    },
}


class TimelineEntry(Enum):
    CURRENT = "current"
    PAST = "past"
    PREDICTED = "predicted"
    TARGET = "target"
    PAST_TARGET = "pastTarget"


class Menu(CWindow):
    def __init__(self):
        super().__init__()
        self._menu_ui = Ui_menu_view()
        self._menu_ui.setupUi(self.placeholder_content)

        self._seed_display_mode = False  # False = 2x8byte, True = 4x4byte

        # Eye tracking progress
        self._tracking_progress = None

        # Countdown
        self._countdown_widget = None
        self._countdown_active = False
        self._countdown_start_at_adv = -1
        self._final_a_press_adv = -1
        self._delay2_start_at_adv = -1
        self._delay2_a_press_adv = -1
        self._countdown_end_at_adv = -1

        self._icons_path = Const.ICONS_DIR

        # Advances timeline
        self.timeline_layout.setAlignment(Qt.AlignTop)
        self.timeline_layout.setContentsMargins(0, 0, 0, 0)
        self.timeline_layout.setSpacing(2)
        self._scroll_area = self._menu_ui.scrollArea
        self._scroll_area.setFocusPolicy(Qt.NoFocus)
        self._scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff)
        self._scroll_area.viewport().installEventFilter(self)
        self._scroll_pending = False
        self._scroll_offset = 0
        self._scroll_anim = QPropertyAnimation(
            self._scroll_area.verticalScrollBar(), b"value")
        self._scroll_anim.setDuration(Const.SCROLL_ANIMATION_DURATION)
        self._scroll_anim.setEasingCurve(QEasingCurve.OutCubic)
        self._scroll_area.verticalScrollBar().rangeChanged.connect(
            self._on_scroll_range_changed)
        self._label_pool = []
        self._center_padding = 0

        self._replace_placeholders()
        self._setup_superqt_widgets()
        self._replace_checkboxes_with_switches(self._menu_ui)
        self._link_buttons()
        self.set_seed_display_mode()
        self.sync_tracking_state(tracking=False, preview=False)

        self.btn_debug.setVisible(Const.DEBUG_MODE)

    def _setup_icons(self):
        super()._setup_icons()
        setup_icons(self, _ICONS, self._icons_path)

    def _replace_placeholders(self):
        # Tracking progress
        placeholder = self._menu_ui.placeholder_tracking_progress
        self._tracking_progress = LinearProgress()
        layout = placeholder.parentWidget().layout()
        layout.replaceWidget(placeholder, self._tracking_progress)
        placeholder.deleteLater()

        # Timer circular progress
        placeholder = self._menu_ui.placeholder_countdown_display
        self._countdown_widget = CircularProgress()
        self._countdown_widget.setVisible(False)
        countdown_policy = QSizePolicy(QSizePolicy.Policy.Expanding,
                                       QSizePolicy.Policy.Expanding)
        self._countdown_widget.setSizePolicy(countdown_policy)
        layout = placeholder.parentWidget().layout()
        layout.replaceWidget(placeholder, self._countdown_widget)
        placeholder.deleteLater()

        # Eye manager gallery
        placeholder = self._menu_ui.placeholder_eye_manager
        self._eye_manager = GalleryContainer(Const.EYES_DIR)
        layout = placeholder.parentWidget().layout()
        layout.replaceWidget(placeholder, self._eye_manager)
        placeholder.deleteLater()

    def _setup_superqt_widgets(self):
        # Reident range double slider
        ds = self.rslider_reident_range
        ds.setOrientation(Qt.Horizontal)
        ds.setRange(Const.REIDENT_MIN, Const.REIDENT_MAX)
        ds.setValue((Const.DF_REIDENT_MIN_VAL, Const.DF_REIDENT_MAX_VAL))

        self.lbl_reident_min.setText(f"{ds.value()[0]:.0f}")
        self.lbl_reident_max.setText(f"{ds.value()[1]:.0f}")

        ds.valueChanged.connect(
            lambda v: (
                self.lbl_reident_min.setText(f"{v[0]:.0f}"),
                self.lbl_reident_max.setText(f"{v[1]:.0f}")
            )
        )

        # Snap: patch _type_cast so ALL values snap to step
        step_value = Const.DF_REIDENT_STEP_VAL
        ds.setSingleStep(step_value)
        ds._type_cast = lambda v: round(
            float(v) / step_value) * step_value

    # Button wiring

    def _link_buttons(self):
        # Tabs
        self.btn_eye_manager.clicked.connect(
            lambda: self._switch_to_tab("EYE_MANAGER"))
        self.btn_configs.clicked.connect(
            lambda: self._switch_to_tab("CONFIGS"))
        self.btn_preferences.clicked.connect(
            lambda: self._switch_to_tab("PREFERENCES"))
        self.btn_debug.clicked.connect(
            lambda: self._switch_to_tab("DEBUG"))

        seed_btns = [
            self.btn_4bytes_seed_0,
            self.btn_4bytes_seed_1,
            self.btn_4bytes_seed_2,
            self.btn_4bytes_seed_3,
            self.btn_8bytes_s0,
            self.btn_8bytes_s1,
        ]

        for btn in seed_btns:
            btn.clicked.connect(self.handle_copy_clicked)

        self.switch_seed_display.clicked.connect(self.toggle_seed_display)
        self.slider_threshold.valueChanged.connect(
            self._update_threholds)

        # Eye Manager Tab
        # TODO - buttons from this tabs

        # Debug Tab
        # TODO - buttons from this tab

    # region Properties

    @property
    def grpb_bottom_bar(self):
        return self._menu_ui.grpb_bottom_bar

    @property
    def btn_eye_manager(self):
        return self._menu_ui.btn_eye_manager

    @property
    def btn_configs(self):
        return self._menu_ui.btn_configs

    @property
    def btn_preferences(self):
        return self._menu_ui.btn_preferences

    @property
    def btn_debug(self):
        return self._menu_ui.btn_debug

    @property
    def spin_advance_target(self):
        return self._menu_ui.spin_advance_target

    @property
    def switch_tracking(self):
        return self._menu_ui.switch_tracking

    @property
    def switch_tracking_tidsid(self):
        return self._menu_ui.switch_tracking_tidsid

    @property
    def btn_reidentify(self):
        return self._menu_ui.btn_reidentify

    @property
    def btn_4bytes_seed_0(self):
        return self._menu_ui.btn_4bytes_s0

    @property
    def btn_4bytes_seed_1(self):
        return self._menu_ui.btn_4bytes_s1

    @property
    def btn_4bytes_seed_2(self):
        return self._menu_ui.btn_4bytes_s2

    @property
    def btn_4bytes_seed_3(self):
        return self._menu_ui.btn_4bytes_s3

    @property
    def btn_8bytes_s0(self):
        return self._menu_ui.btn_8bytes_s0

    @property
    def btn_8bytes_s1(self):
        return self._menu_ui.btn_8bytes_s1

    @property
    def btn_start_countdown(self):
        return self._menu_ui.btn_start_countdown

    @property
    def switch_seed_display(self):
        return self._menu_ui.switch_seed_display

    @property
    def timeline_layout(self):
        return self._menu_ui.list_advance_timeline

    @property
    def spin_final_a_press_delay(self):
        return self._menu_ui.spin_final_a_press_delay

    @property
    def spin_timeline_buffer(self):
        return self._menu_ui.spin_timeline_buffer

    @property
    def lbl_timeline_start(self):
        return self._menu_ui.lbl_timeline_start

    @property
    def lbl_press_a(self):
        return self._menu_ui.lbl_press_a

    @property
    def btn_stop_timeline(self):
        return self._menu_ui.btn_stop_timeline

    @property
    def btn_copy_timeline_adv(self):
        return self._menu_ui.btn_copy_timeline_adv

    @property
    def chkb_plus_one_menu_close(self):
        return self._menu_ui.chkb_plus_one_menu_close

    @property
    def chkb_auto_start_countdown(self):
        return self._menu_ui.chkb_auto_start_countdown

    @property
    def rslider_reident_range(self):
        return self._menu_ui.rslider_reident_range

    @property
    def lbl_reident_min(self):
        return self._menu_ui.lbl_reident_min

    @property
    def lbl_reident_max(self):
        return self._menu_ui.lbl_reident_max

    @property
    def spin_time_delay(self):
        return self._menu_ui.spin_time_delay

    @property
    def spin_advance_delay(self):
        return self._menu_ui.spin_advance_delay

    @property
    def spin_advance_delay_2(self):
        return self._menu_ui.spin_advance_delay_2

    # Noise
    @property
    def chkb_reident_pkmn_npc(self):
        return self._menu_ui.chkb_reident_pkmn_npc

    @property
    def spin_npcs(self):
        return self._menu_ui.spin_npcs

    @property
    def spin_npcs_countdown(self):
        return self._menu_ui.spin_npcs_countdown

    @property
    def spin_pkmn_npcs_countdown(self):
        return self._menu_ui.spin_pkmn_npcs_countdown

    # Eye Manager
    @property
    def switch_preview_tracking(self):
        return self._menu_ui.switch_preview_tracking

    @property
    def btn_create_resource(self):
        return self._menu_ui.btn_create_resource

    @property
    def btn_delete_resource(self):
        return self._menu_ui.btn_delete_resource

    @property
    def tab_widget(self):
        return self._menu_ui.tab_widget

    @property
    def lbl_adv_trgt_eta(self):
        return self._menu_ui.lbl_adv_trgt_eta

    @property
    def slider_threshold(self):
        return self._menu_ui.slider_threshold

    @property
    def lbl_threshold_value(self):
        return self._menu_ui.lbl_threshold_value

    @property
    def eye_gallery(self):
        return self._eye_manager

    # Config Tab
    @property
    def cmb_config(self):
        return self._menu_ui.cmb_config

    @property
    def txt_config_description(self):
        return self._menu_ui.textEdit

    @property
    def lbl_cfg_roi_value(self):
        return self._menu_ui.lbl_cfg_roi_value

    @property
    def lbl_cfg_threshold_value(self):
        return self._menu_ui.lbl_cfg_threshold_value

    @property
    def lbl_cfg_plus_one_menu_close_value(self):
        return self._menu_ui.lbl_cfg_plus_one_menu_close_value

    @property
    def lbl_cfg_final_a_press_delay_value(self):
        return self._menu_ui.lbl_cfg_final_a_press_delay_value

    @property
    def lbl_cfg_timeline_buffer_value(self):
        return self._menu_ui.lbl_timeline_buffer_value

    @property
    def lbl_cfg_npcs_value(self):
        return self._menu_ui.lbl_cfg_npcs_value

    @property
    def lbl_cfg_npcs_cd_value(self):
        return self._menu_ui.lbl_cfg_npcs_cd_value

    @property
    def lbl_cfg_pkmn_npcs_countdown_value(self):
        return self._menu_ui.lbl_cfg_pkmn_npcs_countdown_value

    @property
    def btn_create_config(self):
        return self._menu_ui.btn_create_config

    @property
    def btn_save_config(self):
        return self._menu_ui.btn_save_config

    @property
    def btn_load_config(self):
        return self._menu_ui.btn_load_config

    @property
    def gv_img_preview(self):
        return self._menu_ui.gv_img_preview

    # endregion

    def display_config_image(self, image_path):
        """Show the config's eye image in the preview widget."""
        gv = self.gv_img_preview
        scene = QGraphicsScene(gv)

        if image_path and image_path.exists():
            pixmap = QPixmap(str(image_path))
            scene.addPixmap(pixmap)
        else:
            scene.clear()

        gv.setScene(scene)
        gv.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)

    def display_config(self, cfg):
        """Update config tab labels from a ConfigModel instance."""
        self.txt_config_description.setText(cfg.description)

        roi = cfg.roi
        self.lbl_cfg_roi_value.setText(
            f"[{roi[0]}, {roi[1]}, {roi[2]}, {roi[3]}]")
        self.lbl_cfg_threshold_value.setText(f"{cfg.threshold:.2f}")
        self.lbl_cfg_plus_one_menu_close_value.setText(
            "YES" if cfg.plus_one_menu_close else "NO")
        self.lbl_cfg_final_a_press_delay_value.setText(
            str(cfg.final_a_press_delay))
        self.lbl_cfg_timeline_buffer_value.setText(
            str(cfg.timeline_buffer))
        self.lbl_cfg_npcs_value.setText(str(cfg.npc))
        self.lbl_cfg_npcs_cd_value.setText(str(cfg.timeline_npc))
        self.lbl_cfg_pkmn_npcs_countdown_value.setText(
            str(cfg.pkmn_npc))

    # region Debug Tab

    @property
    def btn_generate_blinks(self):
        return self._menu_ui.btn_generate_blinks

    @property
    def btn_generate_blinks_munchlax(self):
        return self._menu_ui.btn_generate_blinks_munchlax

    # endregion

    def _switch_to_tab(self, tab_name):
        curr_tab_index = self.tab_widget.currentIndex()
        index = _TABS.get(tab_name)

        if curr_tab_index == index:
            self.tab_widget.setCurrentIndex(_TABS["MAIN"])
        elif index is not None:
            self.tab_widget.setCurrentIndex(_TABS[tab_name])

        self._setup_bottom_bar_buttons(tab_name)

    def _setup_bottom_bar_buttons(self, tab_name):
        match tab_name:
            case "MAIN":
                pass
            case "EYE_MANAGER":
                pass
            case "DEBUG":
                pass
            case _:
                pass

    def eventFilter(self, obj, event):
        # Stop wheel scroll in the advance timeline
        if obj is self._scroll_area.viewport():
            if event.type() == QEvent.Type.Wheel:
                return True
            if event.type() == QEvent.Type.Resize:
                self._update_center_padding()

        return super().eventFilter(obj, event)

    def toggle_seed_display(self):
        self._seed_display_mode = not self._seed_display_mode
        self.set_seed_display_mode()

    def set_seed_display_mode(self):
        visible = self._seed_display_mode
        self.btn_4bytes_seed_0.setVisible(visible)
        self.btn_4bytes_seed_1.setVisible(visible)
        self.btn_4bytes_seed_2.setVisible(visible)
        self.btn_4bytes_seed_3.setVisible(visible)

        self.btn_8bytes_s0.setVisible(not visible)
        self.btn_8bytes_s1.setVisible(not visible)

    def sync_tracking_state(self, tracking, preview):
        self.switch_tracking.setEnabled(not preview)
        self.switch_preview_tracking.setEnabled(not tracking)

        self.switch_tracking_tidsid.setVisible(not tracking)
        self.btn_reidentify.setVisible(not tracking)

        set_switch_icon(self, "switch_tracking", _ICONS, self._icons_path,
                        1 if tracking else 0, Const.ICON_DEFAULT_SIZE_BIG)
        self.switch_preview_tracking.setText(
            "STOP" if preview else "PREVIEW")

        self.set_enabled_tracking_progress(tracking)

    def stop_tracking_process(self):
        self._tracking_progress.total_segments = 1
        self._tracking_progress.progress = 0
        self._tracking_progress.setEnabled(False)

    def set_enabled_tracking_progress(self, enabled):
        self._tracking_progress.setEnabled(enabled)
        self._tracking_progress.progress = 0
        if not enabled:
            self._tracking_progress.total_segments = 1

    def set_tracking_progress(self, current, total):
        self._tracking_progress.setEnabled(True)
        self._tracking_progress.total_segments = total
        self._tracking_progress.progress = current

    def handle_copy_clicked(self):
        btn = self.sender()
        Utils.copy_content_to_clipboard(btn.text())

    def start_countdown(self, total_ticks):
        self._countdown_active = True
        self._countdown_widget.total_segments = total_ticks
        self._countdown_widget.progress = total_ticks
        self._countdown_widget.join_colors = True
        self.btn_start_countdown.setEnabled(False)
        self._countdown_widget.setVisible(True)

    def update_countdown(self, remaining):
        self._countdown_widget.progress = max(remaining, 0)

    def stop_countdown(self):
        stop = True
        self._countdown_active = not stop
        self._countdown_end_at_adv = -1
        self._countdown_widget.setVisible(not stop)
        self.btn_start_countdown.setEnabled(stop)

    def display_seed(self, seed_4x32, seed_2x64):
        self.btn_4bytes_seed_0.setText(seed_4x32[0])
        self.btn_4bytes_seed_1.setText(seed_4x32[1])
        self.btn_4bytes_seed_2.setText(seed_4x32[2])
        self.btn_4bytes_seed_3.setText(seed_4x32[3])

        self.btn_8bytes_s0.setText(seed_2x64[0])
        self.btn_8bytes_s1.setText(seed_2x64[1])

    def _update_threholds(self):
        raw_value = self.slider_threshold.value()

        stepped_value = round(raw_value / 5) * 5
        if stepped_value != raw_value:
            self.slider_threshold.setValue(stepped_value)
            return

        value = stepped_value * 0.01
        text = f"{value:.2f}".rstrip('0').rstrip('.')
        self.lbl_threshold_value.setText(text)

    # region Advance timeline
    def _recycle_label(self, label):
        label.hide()
        self._label_pool.append(label)

    def _acquire_label(self, advance, state, blink_type, timer_icon):
        if self._label_pool:
            lbl = self._label_pool.pop()
        else:
            lbl = AdvanceLabel()

        lbl.setText(str(advance))
        lbl.setProperty("timelineState", state.value)
        lbl.append_icon(blink_type)
        lbl.prepend_icon(timer_icon)

        lbl.repolish()
        return lbl

    def _clear_timeline(self):
        layout = self.timeline_layout
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w:
                self._recycle_label(w)

    def _label_count(self):
        return self.timeline_layout.count()

    def _get_timeline_label(self, index):
        item = self.timeline_layout.itemAt(index)
        return item.widget() if item else None

    def _set_entry_state(self, label, state):
        label.setProperty("timelineState", state.value)
        label.repolish()

    def init_timeline(self, current_advance, current_value, predictions):
        container = self._scroll_area.widget() or self._scroll_area
        container.setUpdatesEnabled(False)

        self._clear_timeline()

        self._add_timeline_entry(
            current_advance, current_value, TimelineEntry.CURRENT)

        for adv, val, pred_blink in predictions:
            target = self.spin_advance_target.value()
            adv_type = TimelineEntry.PREDICTED if adv != target \
                else TimelineEntry.TARGET
            self._add_timeline_entry(adv, pred_blink, adv_type)

        container.setUpdatesEnabled(True)
        self._scroll_to_current()

    def push_advance(self, current_advance, _rng, predictions, blink_type):
        layout = self.timeline_layout
        container = self._scroll_area.widget() or self._scroll_area
        container.setUpdatesEnabled(False)

        # Remove old predictions from the end
        removable = {TimelineEntry.PREDICTED.value, TimelineEntry.TARGET.value}
        while self._label_count() > 0:
            idx = self._label_count() - 1
            last = self._get_timeline_label(idx)

            if not (last and last.property("timelineState") in removable):
                break

            w = layout.takeAt(idx).widget()
            self._recycle_label(w)

        # Age previous current > past (or pastTarget if it matches target)
        if self._label_count() > 0:
            prev = self._get_timeline_label(self._label_count() - 1)
            if prev and prev.property("timelineState") == \
                    TimelineEntry.CURRENT.value:
                target = self.spin_advance_target.value()
                is_target = str(target) == prev.text()
                new_state = TimelineEntry.PAST_TARGET if is_target \
                    else TimelineEntry.PAST
                self._set_entry_state(prev, new_state)

        # Trim history
        trimmed_height = 0
        past_advances = max(Const.MAX_ADVANCES_HISTORY, 1)

        while self._label_count() >= past_advances:
            w = layout.takeAt(0).widget()
            trimmed_height += w.sizeHint().height() + layout.spacing()
            self._recycle_label(w)

        self._add_timeline_entry(
            current_advance, blink_type, TimelineEntry.CURRENT)

        # Add predictions (each with its own blink type)
        for adv, val, pred_blink in predictions:
            # target = self.spin_advance_target.value()
            adv_type = self._get_adv_type(adv)
            self._add_timeline_entry(adv, pred_blink, adv_type)

        container.setUpdatesEnabled(True)
        self._scroll_to_current(trimmed_height)

    def _get_adv_type(self, adv):
        target = self.spin_advance_target.value()

        if adv == target:
            return TimelineEntry.TARGET

        # Countdown end marker (only while a countdown is running)
        if self._countdown_active and adv == self._countdown_end_at_adv:
            return TimelineEntry.TARGET

        # Static calibration markers (always visible when configured)
        if self._countdown_start_at_adv > 0:
            if (adv == self._final_a_press_adv or
                    adv == self._delay2_start_at_adv or
                    adv == self._delay2_a_press_adv):
                return TimelineEntry.TARGET

        return TimelineEntry.PREDICTED

    def _add_timeline_entry(self, advance, blink_type, state):
        # Eye icon
        blink_type_icon = blink_type.value if isinstance(
            blink_type, BlinkType) else None

        # Timer icon (only when countdown is configured)
        timer_icon = None
        if (self._countdown_active
                and advance == self._countdown_end_at_adv):
            timer_icon = 1
        elif self._countdown_start_at_adv > 0:
            if advance in (self._final_a_press_adv,
                           self._delay2_a_press_adv):
                timer_icon = 1
            elif advance in (self._countdown_start_at_adv,
                             self._delay2_start_at_adv):
                timer_icon = 0

        lbl = self._acquire_label(
            advance, state, blink_type_icon, timer_icon)
        self.timeline_layout.addWidget(lbl)
        lbl.show()

    def _update_center_padding(self):
        vp_h = self._scroll_area.viewport().height()
        if vp_h != self._center_padding:
            self._center_padding = vp_h
            self.timeline_layout.setContentsMargins(
                0, vp_h, 0, vp_h)

    def _find_current_widget(self):
        for i in range(self._label_count()):
            w = self._get_timeline_label(i)
            if w and w.property("timelineState") == \
                    TimelineEntry.CURRENT.value:
                return w
        return None

    def _calc_scroll_target(self):
        current = self._find_current_widget()
        if current is None:
            return self._scroll_area.verticalScrollBar().maximum()
        container = self._scroll_area.widget()
        if container is None:
            return 0
        item_y = current.mapTo(container, current.rect().topLeft()).y()
        # Offset upward so past entries remain visible above current
        past_height = self._calc_past_height()
        return max(0, item_y - past_height)

    def _calc_past_height(self):
        """Height of all past/pastTarget entries above current."""
        layout = self.timeline_layout
        total = 0
        for i in range(self._label_count()):
            w = self._get_timeline_label(i)
            if not w:
                continue
            state = w.property("timelineState")
            if state not in (TimelineEntry.PAST.value,
                             TimelineEntry.PAST_TARGET.value):
                break
            total += w.sizeHint().height() + layout.spacing()
        return total

    def _scroll_to_current(self, offset=0):
        self._scroll_pending = True
        self._scroll_offset = offset
        self._update_center_padding()
        if offset > 0:
            QTimer.singleShot(0, self._animate_to_current)

    def _on_scroll_range_changed(self, _min, _max):
        self._animate_to_current()

    def _animate_to_current(self):
        if not self._scroll_pending:
            return
        self._scroll_pending = False
        sb = self._scroll_area.verticalScrollBar()
        target = self._calc_scroll_target()
        start = max(0, sb.value() - self._scroll_offset)
        self._scroll_offset = 0
        sb.setValue(start)
        self._scroll_anim.stop()
        self._scroll_anim.setStartValue(start)
        self._scroll_anim.setEndValue(target)
        if start != target:
            self._scroll_anim.start()

    # endregion
