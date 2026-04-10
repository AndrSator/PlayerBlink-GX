import sys
import time
import configparser

import cv2

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QDialog

from src import CvControl, EyeTracker, AdvanceManager, \
    Calc, Xorshift

from src.log import logger
from src.utils import Utils
from src.preferences import Preferences
from src.config_model import ConfigModel
from src.eye_manager import EyeManager
from src.constants import Constants as Const

from src.views.tv_window import TvWindow
from src.views.menu import Menu

from src.widgets.cgallery import FileNameDialog

__version__ = "1.0.0"


class Controller:
    """ Mediates between logic and views """

    def __init__(self):
        super().__init__()

        # Frame polling timer
        prefs = Preferences()
        poll_ms = prefs.display_poll_ms
        if poll_ms <= 0:
            poll_ms = max(1, 1000 // prefs.capture_fps)
        self._timer = QTimer()
        self._timer.setTimerType(Qt.PreciseTimer)
        self._timer.timeout.connect(self._poll_frame)
        self._timer.start(poll_ms)

        self._tracking_area = None
        self._refreshing_windows = False
        self._was_paused_before_crop = False
        self._reidentifying = False
        self._reident_noisy = False
        self._tracking_tidsid = False

        self._setup_signals()
        self._link_buttons()
        self.refresh_devices()
        self._sync_eye_controls()
        self._populate_configs()

    # region Signal connections

    def _setup_signals(self):
        # Video
        cvc.capture_started.connect(self.on_capture_started)
        cvc.window_minimized.connect(self.on_window_minimized)

        # AdvanceManager
        am.advance_tick.connect(self._on_advance_tick)
        am.countdown_tick.connect(self._on_countdown_tick)
        am.countdown_finished.connect(self._on_countdown_finished)
        am.auto_start_countdown.connect(self.handle_countdown)

        # EyeTracker
        et.blink_detected.connect(self.on_blink_detected)
        et.tracking_finished.connect(self.on_tracking_finished)
        et.tracking_error.connect(self.on_tracking_error)
        et.match_updated.connect(self.on_match_updated)

        # View
        tvw.crop_started.connect(self.on_crop_started)
        tvw.crop_finished.connect(self.on_crop_finished)
        tvw.tracking_area_defined.connect(self.on_tracking_area_defined)
        tvw.eye_cropped.connect(self.on_eye_cropped)

        # Eye Manager
        m.eye_gallery.selection_changed.connect(self.on_eye_selection_changed)
        em.selected_changed.connect(self._on_eye_resource_changed)

        # Config
        cfm.config_loaded.connect(self._on_config_loaded)
    # endregion

    # Button wiring

    def _link_buttons(self):
        # Main menu buttons
        m.switch_tracking.clicked.connect(self.toggle_tracking)
        m.switch_preview_tracking.clicked.connect(self.toggle_preview_tracking)
        m.switch_tracking_tidsid.clicked.connect(self.tracking_munchlax)
        m.btn_reidentify.clicked.connect(self.reidentify)
        m.btn_stop_timeline.clicked.connect(am.stop_simulating)

        # Advance calibration labels
        m.spin_advance_target.valueChanged.connect(
            self.update_timeline_labels)
        m.spin_final_a_press_delay.valueChanged.connect(
            self.update_timeline_labels)
        m.spin_timeline_buffer.valueChanged.connect(
            self.update_timeline_labels)

        # Options
        m.chkb_plus_one_menu_close.toggled.connect(lambda checked: setattr(
            am, 'inc_one_on_close', checked))
        m.chkb_auto_start_countdown.toggled.connect(
            lambda checked: (
                setattr(am, 'countdown_auto_start', checked),
                m.btn_start_countdown.setEnabled(not checked)
            )
        )
        m.rslider_reident_range.valueChanged.connect(
            self._on_reident_range_changed)

        # NPC settings
        m.spin_npcs.valueChanged.connect(
            lambda v: setattr(am, 'npc_count', v))
        m.spin_npcs_countdown.valueChanged.connect(
            lambda v: setattr(am, 'npc_in_timeline', v))
        m.spin_pkmn_npcs_countdown.valueChanged.connect(
            lambda v: setattr(am, 'npc_pkmn_count', v))

        # Time and advance delay
        m.spin_time_delay.valueChanged.connect(lambda: setattr(
            am, "time_delay", m.spin_time_delay.value()))
        m.spin_advance_delay.valueChanged.connect(lambda: setattr(
            am, "advance_delay", m.spin_advance_delay.value()))
        m.spin_advance_delay_2.valueChanged.connect(lambda: setattr(
            am, "advance_delay_2", m.spin_advance_delay_2.value()))
        m.spin_npcs.valueChanged.connect(
            lambda: self._check_advance_is_targetable)

        # Eye Manager
        m.btn_create_resource.clicked.connect(self.create_eye_resource)
        m.btn_delete_resource.clicked.connect(self.delete_eye_resource)

        # Config tab
        m.cmb_config.currentIndexChanged.connect(self._on_config_selected)
        m.btn_create_config.clicked.connect(self.create_config)
        m.btn_save_config.clicked.connect(self.save_config)
        m.btn_load_config.clicked.connect(self.apply_config)

        # Countdown
        m.btn_start_countdown.clicked.connect(self.handle_countdown)

        # Display controls
        tvw.btn_device_prev.clicked.connect(self.prev_device)
        tvw.btn_device_next.clicked.connect(self.next_device)
        tvw.btn_device_refresh.clicked.connect(self.refresh_devices)
        tvw.btn_adjust_screen.clicked.connect(tvw.adjust_screen)
        tvw.switch_capture.clicked.connect(self.toggle_capture)
        tvw.switch_pause.clicked.connect(self.toggle_pause)
        tvw.switch_crop_tracking_area.clicked.connect(
            tvw.toggle_crop_tracking_area)
        tvw.switch_crop_eye.clicked.connect(tvw.toggle_crop_eye)
        tvw.switch_monitor_mode.clicked.connect(self.toggle_monitor_mode)
        tvw.cmb_windows_list.currentIndexChanged.connect(
            self.on_window_selected)

        # Debug
        m.btn_generate_blinks.clicked.connect(self.debug_generate_blinks)

    def _on_reident_range_changed(self, values):
        am.min_reident = int(values[0])
        am.max_reident = int(values[1])

    # Capture toggle
    def toggle_capture(self):
        if cvc.is_active() or cvc.in_error():
            cvc.stop_capture()
            tvw.clear_display()
        else:
            if cvc.monitor_mode:
                # Pick the currently selected window from the combobox
                title = tvw.cmb_windows_list.currentText()
                if title:
                    try:
                        cvc.set_window_by_title(title)
                    except ValueError:
                        pass
            cvc.start_capture()
        self._sync_view()

    def toggle_pause(self):
        if cvc.is_paused():
            cvc.resume_capture()
        elif cvc.is_capturing():
            cvc.pause_capture()
        self._sync_view()

    # Crop signals from the view
    def on_crop_started(self):
        self._was_paused_before_crop = cvc.is_paused()
        if cvc.is_capturing():
            cvc.pause_capture()
            self._sync_view()

    def on_crop_finished(self):
        if not self._was_paused_before_crop:
            cvc.resume_capture()
            self._sync_view()

    def on_tracking_area_defined(self, x, y, w, h):
        self._tracking_area = (x, y, w, h)
        et.tracking_area = (x, y, w, h)
        logger.debug(f"[Controller] Tracking area: x={x}, y={y}, w={w}, h={h}")
        self._sync_view()

    # region Eye Resource Management

    def create_eye_resource(self):
        dialog = FileNameDialog(m)

        if dialog.exec() == QDialog.Accepted:
            name = dialog.get_name()

            if not name:
                return  # o puedes mostrar error

            file_name = f"{name}.png"

            ok = em.create_resource(file_name)
            if not ok:
                return

            m.eye_gallery.reload_items()

    def delete_eye_resource(self):
        resource = m.eye_gallery.selected_resource
        if resource is None:
            return

        em.delete_selected()
        m.eye_gallery.remove_selected()
        self._sync_eye_controls()
        logger.info(f"[Controller] Deleted eye resource: {resource.name}")

    def on_eye_cropped(self, cropped_array):
        resource = em.selected_resource
        if resource is None:
            return

        cv2.imwrite(str(resource.path), cropped_array)
        logger.info(f"[Controller] Overwritten eye crop: {resource.path}")
        m.eye_gallery.reload_selected()
        self._load_eye_pattern()

    def on_eye_selection_changed(self, resource):
        em.selected_resource = resource

    def _on_eye_resource_changed(self, _resource):
        self._load_eye_pattern()
        self._sync_eye_controls()

    def _load_eye_pattern(self):
        pattern = em.load_selected_pattern()
        if pattern is not None:
            try:
                et.img_pattern_sample = pattern
                logger.debug("[Controller] Eye pattern loaded from "
                             f"{em.selected_resource.name}")
            except ValueError as e:
                logger.error(f"[Controller] Failed to load eye pattern: {e}")

    def _sync_eye_controls(self):
        has_selected = em.selected_resource is not None
        # capturing = cvc.is_capturing() or cvc.is_paused()
        has_area = self._tracking_area is not None
        idle = not et.is_tracking() and not et.is_preview()

        # Crop eye requires selected resource + tracking area, and the
        # tracker must be idle (no tracking / reidentify / preview running)
        tvw.switch_crop_eye.setEnabled(has_selected and has_area and idle)

        tracking = et.is_tracking()
        preview = et.is_preview()

        # Switches act as toggles: enabled to start OR to stop
        can_start = has_selected and has_area and idle
        m.switch_tracking.setEnabled(tracking or can_start)
        m.switch_tracking_tidsid.setEnabled(tracking or can_start)
        m.switch_preview_tracking.setEnabled(preview or can_start)
        m.btn_reidentify.setEnabled(
            can_start and am.seed is not None)

        m.btn_delete_resource.setEnabled(has_selected)

        # Countdown only available when simulation is running
        m.btn_start_countdown.setEnabled(am.is_running())

    # endregion

    # region EyeTracker
    def toggle_tracking(self):
        if et.is_tracking():
            et.stop()
            self._tracking_tidsid = False
            self._reidentifying = False
        else:
            et.size = Const.BLINKS_REQUIRED_TRACKING
            m.set_tracking_progress(0, Const.BLINKS_REQUIRED_TRACKING)
            et.start_tracking(cvc)
            am.stop_simulating()
        self._sync_tracking_ui()

    def tracking_munchlax(self):
        if et.is_tracking():
            et.stop()
            self._tracking_tidsid = False
            self._sync_tracking_ui()
            return

        self._tracking_tidsid = True
        size = Const.BLINKS_REQUIRED_TRACKING_TIDSID
        m.set_tracking_progress(0, size)
        et.size = size
        et.start_tracking(cvc)
        am.stop_simulating()
        self._sync_tracking_ui()

    def reidentify(self):
        if am.seed is None:
            logger.debug("[Controller] No seed to reidentify from")
            return

        am.stop_simulating()

        if et.is_active():
            et.stop()
            self._reidentifying = False
            self._reident_noisy = False
            self._sync_tracking_ui()
            return

        self._reidentifying = True
        self._reident_noisy = m.chkb_reident_pkmn_npc.isChecked()

        size = Const.BLINKS_REQUIRED_REIDENTIFY
        if self._reident_noisy:
            size = Const.BLINKS_REQUIRED_REIDENTIFY_NOISY

        m.set_tracking_progress(0, size)
        et.size = size
        et.start_tracking(cvc)
        self._sync_tracking_ui()

    def toggle_preview_tracking(self):
        if et.is_preview():
            et.stop()
        else:
            et.start_preview(cvc)
        self._sync_tracking_ui()

    def _sync_tracking_ui(self):
        idle = not et.is_tracking() and not et.is_preview()
        tracking = et.is_tracking()
        preview = et.is_preview()

        m.sync_tracking_state(tracking, preview)

        # Disable controls related with the video capture
        not_tracking = not tracking
        tvw.switch_pause.setEnabled(not_tracking)
        tvw.switch_crop_tracking_area.setEnabled(not_tracking)
        tvw.switch_capture.setEnabled(idle)
        tvw.switch_monitor_mode.setEnabled(idle)
        tvw.set_devices_controls(idle)
        tvw.cmb_windows_list.setEnabled(idle)
        tvw.btn_device_refresh.setEnabled(idle)
        tvw.tracking = tracking

        self._sync_eye_controls()
        self._sync_config_controls()

        if idle:
            tvw.set_eye_match(None)
            self._sync_view()

    def on_blink_detected(self, blink_type, interval, count, total):
        if count == -1:
            # Preview mode
            kind = "double" if blink_type == 1 else "single"
            logger.info(f"[Preview] Blink detected: {kind}, int={interval}")
            return

        if blink_type == 1:
            # Double blinks are overwritten and emitted twice
            return

        logger.info(f"Blink logged | int: {interval:<2} | "
                    f"{count:>2}/{total:<2}")
        m.set_tracking_progress(count, total)

    def on_tracking_finished(self, blinks, intervals, raw_intervals,
                             offset_time, _end_time):
        logger.info(f"[EyeTracker] Tracking finished: {len(blinks)} blinks")
        logger.debug(f"  blinks:    {blinks}")
        logger.debug(f"  intervals: {intervals}")
        logger.debug(f"  offset:    {offset_time}")
        self._sync_tracking_ui()

        if self._reidentifying:
            self._handle_reidentify(intervals, offset_time)
        elif self._tracking_tidsid:
            self._handle_identify_tidsid(raw_intervals, offset_time)
        else:
            self._handle_identify(blinks, intervals, offset_time)

    def _handle_identify(self, blinks, intervals, offset_time):
        """ First-time seed recovery from 40 blinks """
        t_enter = time.perf_counter()
        logger.debug(
            f"[TIMING identify] enter={t_enter:.3f}, "
            f"offset_time={offset_time:.3f}, "
            f"delta_since_offset={t_enter - offset_time:.3f}s")

        try:
            raw_intervals = intervals[1:]
            npc = am.npc_count

            if npc > 0:
                raw_intervals = [x * (npc + 1) for x in raw_intervals]

            advanced_frame = sum(raw_intervals)
            states = Calc().reverse_states(blinks, raw_intervals)
            seed = Xorshift(*states).get_state()

            # Validate and find the correct NPC phase (distance).
            # With NPCs, the player's blinks land on one of (npc+1)
            # slots. Try each offset until the expected blinks match.
            if npc > 0:
                found = False

                for distance in range(npc + 1):
                    prng = Xorshift(*seed)
                    seq = prng.get_next_rand_sequence(
                        advanced_frame * npc)
                    expected = [
                        r & 0xF for r in seq[distance::npc + 1]
                        if (r & Const.BLINK_BIT_MASK) == 0
                    ]

                    if all(o == e for o, e in zip(blinks, expected)):
                        advanced_frame += distance
                        found = True
                        logger.debug(
                            f"[Controller] NPC phase distance={distance}")
                        break

                if not found:
                    logger.error(
                        "[Controller] NPC phase validation failed")
                    raise ValueError("NPC phase validation failed")

                am.npc_phase_distance = distance

            result = Xorshift(*seed)
            result.get_next_rand_sequence(advanced_frame)

            am.set_seed(*result.get_state())

        except Exception as e:
            logger.error(f"[Controller] Failed to recover seed: {e}")
            return

        t_seed = time.perf_counter()
        logger.debug(f"[TIMING identify] seed_done={t_seed:.3f}, "
                     f"seed_cost={t_seed - t_enter:.3f}s")

        # Auto-calibrate tick rate from observed blink timing
        if am.auto_calibrate and et.calibrated_tick is not None:
            am.tick_rate = et.calibrated_tick
            logger.debug(
                f"[CALIBRATION] tick_rate={am.tick_rate:.6f}s "
                f"(default={Const.FRAME_CORRECTION}, "
                f"delta={am.tick_rate - Const.FRAME_CORRECTION:+.6f}s)")

        # Compensate elapsed time BEFORE displaying seed
        # (matches legacy: rng advances but counter stays at initial)
        anchor = am.compensate_elapsed(offset_time)

        s4 = am.get_seed_4x32()
        s2 = am.get_seed_2x64()
        logger.info(f"[Controller] Seed S[0-1]: {' '.join(s2)}")
        logger.info(f"[Controller] Seed S[0-3]: {' '.join(s4)}")
        m.display_seed(s4, s2)

        predictions = am.predict_next(Const.OFFSET_ADVANCES_PREDICTION)
        m.init_timeline(am.advances, 0, predictions)

        t_ui = time.perf_counter()
        logger.debug(
            f"[TIMING identify] ui_done={t_ui:.3f}, "
            f"ui_cost={t_ui - t_seed:.3f}s")

        logger.debug(f"[TIMING identify] advances_before_tick={am.advances}")
        am.start_tick_loop(anchor)
        self._sync_eye_controls()
        # et.start_preview(cvc)

    def _handle_identify_tidsid(self, raw_intervals, offset_time):
        """ Seed recovery from 64 munchlax blink intervals (float secs) """
        self._tracking_tidsid = False
        t_enter = time.perf_counter()
        logger.debug(
            f"[TIMING tidsid] enter={t_enter:.3f}, "
            f"offset_time={offset_time:.3f}, "
            f"delta_since_offset={t_enter - offset_time:.3f}s")
        logger.debug(
            f"  raw_intervals: "
            f"{[f'{v:.3f}' for v in raw_intervals]}")

        try:
            advances = len(raw_intervals)
            calc = Calc()

            # Correct for observation delay and skip first interval
            corrected = [iv + 0.048 for iv in raw_intervals]
            corrected = corrected[1:]

            states = calc.reverse_states_by_munchlax(corrected)

            # Validation: compare expected vs observed intervals
            prng = Xorshift(*states)
            expected = [
                calc.randrange(r, 100, 370) / 30
                for r in prng.get_next_rand_sequence(advances)
            ]
            paired = list(zip(corrected, expected))

            if not all(abs(o - e) < 0.1 for o, e in paired):
                logger.error(
                    "[Controller] TID/SID validation failed: "
                    "intervals don't match")
                raise ValueError("TID/SID interval validation failed")

            # Advance to current state
            result = Xorshift(*Xorshift(*states).get_state())
            result.get_next_rand_sequence(len(corrected))

            am.set_seed(*result.get_state())

        except Exception as e:
            logger.error(f"[Controller] TID/SID seed recovery failed: {e}")
            return

        t_seed = time.perf_counter()
        logger.debug(f"[TIMING tidsid] seed_done={t_seed:.3f}, "
                     f"seed_cost={t_seed - t_enter:.3f}s")

        # Compensate elapsed time
        anchor = am.compensate_elapsed(offset_time)

        s4 = am.get_seed_4x32()
        s2 = am.get_seed_2x64()
        logger.info(f"[Controller] TID/SID Seed S[0-1]: {' '.join(s2)}")
        logger.info(f"[Controller] TID/SID Seed S[0-3]: {' '.join(s4)}")
        m.display_seed(s4, s2)

        predictions = am.predict_next(Const.OFFSET_ADVANCES_PREDICTION)
        m.init_timeline(am.advances, 0, predictions)

        t_ui = time.perf_counter()
        logger.debug(
            f"[TIMING tidsid] ui_done={t_ui:.3f}, "
            f"ui_cost={t_ui - t_seed:.3f}s")

        logger.debug(
            f"[TIMING tidsid] advances_before_tick={am.advances}")
        am.start_tick_loop(anchor)
        self._sync_eye_controls()

    def _handle_reidentify(self, intervals, offset_time):
        noisy = self._reident_noisy
        self._reidentifying = False
        self._reident_noisy = False
        t_enter = time.perf_counter()
        logger.debug(
            f"[TimingReident] enter={t_enter:.3f}, "
            f"offset_time={offset_time:.3f}, "
            f"delta_since_offset={t_enter - offset_time:.3f}s, "
            f"noisy={noisy}")

        try:
            if noisy:
                result = am.find_position_by_intervals_noisy(intervals)
            else:
                result = am.find_position_by_intervals(intervals)

            if result is None:
                logger.debug(
                    "[Controller] Reidentification failed: position not found")
                return

            rng, advance = result

            t_search = time.perf_counter()
            logger.debug(
                f"[TimingReident] search_done={t_search:.3f}, "
                f"search_cost={t_search - t_enter:.3f}s, "
                f"found_advance={advance}")

            am.reidentify(rng, advance)

        except Exception as e:
            logger.error(f"[Controller] Reidentification error: {e}")
            return

        # Compensate elapsed time BEFORE displaying seed.
        # Reidentify counts elapsed advances (legacy behaviour)
        anchor = am.compensate_elapsed(offset_time, count_advances=True)

        s4 = am.get_seed_4x32()
        s2 = am.get_seed_2x64()
        logger.info(f"[Controller] Reidentified at advance {am.advances}")
        logger.info(f"[Controller] Seed S[0-3]: {' '.join(s4)}")
        logger.info(f"[Controller] Seed S[0-1]: {' '.join(s2)}")
        m.display_seed(s4, s2)

        predictions = am.predict_next(Const.OFFSET_ADVANCES_PREDICTION)
        m.init_timeline(am.advances, 0, predictions)

        t_ui = time.perf_counter()
        logger.debug(
            f"[TimingReident] ui_done={t_ui:.3f}, "
            f"ui_cost={t_ui - t_search:.3f}s")

        logger.debug(f"[TimingReident] advances_before_tick={am.advances}")
        am.start_tick_loop(anchor)
        self._sync_eye_controls()

        self._check_advance_is_targetable()
        self._update_adv_trgt_eta_label()

        # et.start_preview(cvc)

    def on_tracking_error(self, message):
        logger.error(f"[EyeTracker] Error: {message}")
        self._sync_tracking_ui()

    def on_match_updated(self, is_matching, x, y, w, h):
        if is_matching:
            tvw.set_eye_match((x, y, w, h))
            return

        tvw.set_eye_match(None)

    def _on_advance_tick(self, advances, rng, npc_blinks, predictions):
        self._update_adv_trgt_eta_label()

        # Get player blink info from RNG
        player_blink = Utils.blink_from_rng(rng)
        blink_str = f" | PLYR: {player_blink.name}" if player_blink else ""

        # Get NPCs blinks
        npc_str = ""
        for idx, bt in npc_blinks:
            npc_str += f" | NPC{idx}: {bt.name}"

        logger.info(f"{rng:08X}| Advance: {advances}{blink_str}{npc_str}")

        # When NPCs configured, show NPC[0] blink only; otherwise player
        if am.npc_count > 0:
            blink_type = None
            if npc_blinks and npc_blinks[0][0] == 0:
                blink_type = npc_blinks[0][1]
        else:
            blink_type = player_blink

        m.push_advance(advances, rng, predictions, blink_type)

    # endregion

    # region Device navigation
    def prev_device(self):
        cvc.set_prev_device()
        self.update_current_device()

    def next_device(self):
        cvc.set_next_device()
        self.update_current_device()

    def update_current_device(self):
        device = cvc.current_device
        if device is None:
            tvw.set_no_input()
            return

        cvc.start_capture()
        tvw.set_device_name(device.name)
        tvw.set_devices_controls()

    def refresh_devices(self):
        cvc.setup_devices()
        if cvc.current_device is None:
            tvw.set_no_input()
            return

        self.update_current_device()
        tvw.set_devices_controls()

    # endregion

    # region Monitor mode
    def on_window_selected(self, index):
        if index < 0 or self._refreshing_windows:
            return

        title = tvw.cmb_windows_list.currentText()
        if not title:
            return

        try:
            cvc.set_window_by_title(title)
            cvc.start_capture()
        except ValueError as e:
            logger.error(f"[Controller] {e}")
            tvw.set_error_text()

    def toggle_monitor_mode(self):
        enabled = cvc.toggle_monitor_mode()

        if not enabled:
            cvc.stop_capture()
            self.update_current_device()

        tvw.set_monitor_mode(enabled)

        if enabled:
            cvc.stop_capture()
            tvw.clear_display()
            self.refresh_windows()

            if tvw.cmb_windows_list.count() > 0:
                self.on_window_selected(0)
            else:
                tvw.set_no_windows_text()
                tvw.cmb_windows_list.setEnabled(False)

    def refresh_windows(self):
        if sys.platform != 'win32':
            return

        if not cvc.monitor_mode:
            return

        cvc.setup_windows()
        windows = cvc.get_windows_titles()

        self._refreshing_windows = True
        tvw.populate_window_menu(windows if windows else [])
        tvw.cmb_windows_list.setEnabled(bool(windows))
        self._refreshing_windows = False

    def on_capture_started(self, ok):
        if not ok:
            tvw.set_error_text()
            if cvc.monitor_mode:
                cvc.current_window = None
                self.refresh_windows()
        else:
            tvw.clear_error_text()
        self._sync_view()

    def on_window_minimized(self, minimized):
        if minimized:
            tvw.set_minimized_text()
        else:
            tvw.clear_error_text()

    def _poll_frame(self):
        frame = cvc.read_frame()
        if frame is not None:
            tvw.push_frame(frame)

    def _sync_view(self):
        capturing = cvc.is_capturing() or cvc.is_paused()
        paused = cvc.is_paused()
        tvw.update_switch_icons(capturing, paused)
        self._sync_eye_controls()

    # region Countdown
    def update_timeline_labels(self):
        # Calcs for countdown auto-start and final A press timing
        trgt = m.spin_advance_target.value()
        timeline_buffer = m.spin_timeline_buffer.value()
        final_a_press_value = m.spin_final_a_press_delay.value()

        m._countdown_start_at_adv = trgt - timeline_buffer
        m._final_a_press_adv = trgt - final_a_press_value

        lbl_timeline_visible = (timeline_buffer > 0 and
                                m._countdown_start_at_adv != trgt and
                                m._countdown_start_at_adv > 0)
        final_a_press_visible = (final_a_press_value > 0 and
                                 m._final_a_press_adv != trgt and
                                 m._final_a_press_adv > 0)

        lbl_visibles = lbl_timeline_visible and final_a_press_visible

        m.lbl_timeline_start.setText(str(m._countdown_start_at_adv))
        m.lbl_press_a.setText(str(m._final_a_press_adv))

        m.lbl_timeline_start.setVisible(lbl_visibles)
        m.lbl_press_a.setVisible(lbl_visibles)

        am.countdown_auto_start_adv = m._countdown_start_at_adv

        self._check_advance_is_targetable()
        self._update_adv_trgt_eta_label()

    def _check_advance_is_targetable(self):
        # Calcs for NPC
        trgt = m.spin_advance_target.value()

        is_targetable = True

        if (am.simulating):
            if (trgt < am.advances):
                is_targetable = False
                logger.warning(
                    f"[Controller] Advance {trgt} already past")
            elif (trgt - am.advances) % (am.npc_count + 1) != 0:
                is_targetable = False
                logger.warning(
                    f"[Controller] Advance {trgt} is not targetable")

        m.spin_advance_target.setProperty("error", not is_targetable)
        m.spin_advance_target.style().polish(m.spin_advance_target)
        m.spin_advance_target.update()

    # TODO - Actualizar el label a tiempo real, no por ticks
    def _update_adv_trgt_eta_label(self):
        trgt = m.spin_advance_target.value()

        if am.advances == 0 or trgt < am.advances or not am.simulating:
            m.lbl_adv_trgt_eta.setText("")
            return

        remaining = trgt - am.advances
        advances_per_sec = 1 / am.tick_rate
        eta_seconds = remaining * advances_per_sec
        m.lbl_adv_trgt_eta.setText(Utils.format_time(eta_seconds))

    def handle_countdown(self):
        if not am.is_running():
            logger.debug("[Controller] Cannot start countdown: not simulating")
            return

        total = Const.COUNTDOWN_DURATION_SECONDS
        logger.info(f"[Controller] Starting countdown: {total} game ticks")
        m.start_countdown(total)
        am.start_countdown(total)

    def _on_countdown_tick(self, remaining):
        m.update_countdown(remaining)

    def _on_countdown_finished(self, advances, predictions):
        logger.info(
            f"[Controller] Countdown finished, "
            f"timeline rebuilt at advance {advances}")
        m.stop_countdown()
        m.init_timeline(advances, 0, predictions)

    # endregion

    # region Config Management

    def _populate_configs(self):
        configs = cfm.list_configs()
        m.cmb_config.blockSignals(True)
        m.cmb_config.clear()

        for filename in configs:
            display_name = cfm.peek_name(filename)
            m.cmb_config.addItem(display_name, userData=filename)

        m.cmb_config.blockSignals(False)

        if configs:
            m.cmb_config.setCurrentIndex(0)
            cfm.load(configs[0])

        self._sync_config_controls()

    def _on_config_selected(self, index):
        if index < 0:
            return
        filename = m.cmb_config.currentData()
        if filename:
            cfm.load(filename)

    def _on_config_loaded(self, cfg):
        m.display_config(cfg)
        image_path = Const.EYES_DIR / cfg.image
        m.display_config_image(image_path)
        self._sync_config_controls()

    def _sync_config_controls(self):
        busy = et.is_tracking() or et.is_preview()
        has_config = cfm.current_file is not None
        m.btn_load_config.setEnabled(has_config and not busy)
        m.btn_save_config.setEnabled(has_config)

    def create_config(self):
        dialog = FileNameDialog(m)

        if dialog.exec() == QDialog.Accepted:
            name = dialog.get_name()
            if not name:
                return

            filename = cfm.create(name)
            if not filename:
                return

            m.cmb_config.blockSignals(True)
            m.cmb_config.addItem(name, userData=filename)
            idx = m.cmb_config.count() - 1
            m.cmb_config.setCurrentIndex(idx)
            m.cmb_config.blockSignals(False)

            cfm.load(filename)

    def save_config(self):
        if cfm.current_file is None:
            return

        # Read current values from UI controls into the model
        cfm.plus_one_menu_close = m.chkb_plus_one_menu_close.isChecked()
        cfm.final_a_press_delay = m.spin_final_a_press_delay.value()
        cfm.timeline_buffer = m.spin_timeline_buffer.value()
        cfm.threshold = et.threshold
        cfm.time_delay = m.spin_time_delay.value()
        cfm.advance_delay = m.spin_advance_delay.value()
        cfm.advance_delay_2 = m.spin_advance_delay_2.value()
        cfm.npc = m.spin_npcs.value()
        cfm.pkmn_npc = m.spin_pkmn_npcs_countdown.value()
        cfm.timeline_npc = m.spin_npcs_countdown.value()

        if self._tracking_area:
            cfm.roi = list(self._tracking_area)

        # Save current eye resource name
        if em.selected_resource is not None:
            cfm.image = em.selected_resource.name

        cfm.save()
        # Refresh preview labels and image
        m.display_config(cfm)
        m.display_config_image(Const.EYES_DIR / cfm.image)
        logger.info(f"[Controller] Config saved: {cfm.current_file}")

    def apply_config(self):
        if cfm.current_file is None:
            return

        if et.is_tracking() or et.is_preview():
            logger.warning(
                "[Controller] Cannot load config while tracking is active")
            return

        # Apply config values to UI controls and logic
        m.chkb_plus_one_menu_close.setChecked(cfm.plus_one_menu_close)
        am.inc_one_on_close = cfm.plus_one_menu_close

        m.spin_final_a_press_delay.setValue(cfm.final_a_press_delay)
        m.spin_timeline_buffer.setValue(cfm.timeline_buffer)
        m.spin_time_delay.setValue(cfm.time_delay)
        m.spin_advance_delay.setValue(cfm.advance_delay)
        m.spin_advance_delay_2.setValue(cfm.advance_delay_2)

        # NPC settings
        m.spin_npcs.setValue(cfm.npc)
        m.spin_pkmn_npcs_countdown.setValue(cfm.pkmn_npc)
        m.spin_npcs_countdown.setValue(cfm.timeline_npc)

        # Threshold
        et.threshold = cfm.threshold

        # ROI / tracking area
        roi = cfm.roi
        if any(v != 0 for v in roi):
            self._tracking_area = tuple(roi)
            et.tracking_area = tuple(roi)
            tvw.apply_tracking_area(*roi)

        # Select eye resource in gallery (triggers pattern load via signal)
        if not m.eye_gallery.select_by_name(cfm.image):
            logger.warning(
                f"[Controller] Config image not in gallery: {cfm.image}")

        logger.info(
            f"[Controller] Config applied: {cfm.name} ({cfm.current_file})")

    # endregion

    # region Debug / Test
    def debug_generate_blinks(self):
        import random

        logger.debug("[Debug] Generating debug blinks")
        blinks = [0, 1, 0, 0, 1, 0, 0, 0, 1, 0] * 4
        intervals = [random.randint(1, 10) for _ in range(len(blinks))]
        offset_time = time.perf_counter() - 10.0

        et.tracking_finished.emit(
            blinks, intervals, offset_time, None, time.perf_counter())

    # endregion

# region Theme loading


def load_theme():
    try:
        # Load all fonts from the fonts directory
        for font in Const.FONTS_DIR.glob("*.ttf"):
            logger.debug(f"[Theme] Loading font {font.name!r}")
            font_id = QFontDatabase.addApplicationFont(str(font))
            if font_id == -1:
                logger.warning(f"[Theme] Failed to load font {font.name!r}")

        config = configparser.ConfigParser()
        config.optionxform = str  # keep camelCase
        config.read(pref.theme)

        if "colors" not in config:
            raise ValueError("Missing [colors] section in theme file.")

        theme = config["colors"]

        with open(Const.QSS_FILE, "r") as f:
            logger.debug(f"[Theme] Loading QSS from {Const.QSS_FILE!r}")
            qss = f.read()

        for key, value in theme.items():
            # logger.debug(f"[Theme] Applying theme color: {key}={value}")
            qss = qss.replace(f"{{{key}}}", value)

        return qss
    except Exception as e:
        logger.error(f"[Theme] Error loading theme: {e}")
        return ""

# endregion


def show_windows(menu, tv_window):
    theme = load_theme()
    app.setStyleSheet(theme)

    menu.show()
    original_pos = menu.geometry()
    tv_window.move(original_pos.x() + original_pos.width(), original_pos.y())
    tv_window.show()


if __name__ == "__main__":
    QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.Round)
    app = QtWidgets.QApplication(sys.argv)

    pref = Preferences()

    cvc = CvControl()
    et = EyeTracker()
    am = AdvanceManager()
    em = EyeManager(Const.EYES_DIR)
    cfm = ConfigModel()

    m = Menu()
    tvw = TvWindow()

    c = Controller()

    QTimer.singleShot(0, lambda: show_windows(m, tvw))

    sys.exit(app.exec())
