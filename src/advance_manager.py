import time
import heapq

from threading import Thread

from PySide6.QtCore import QObject, Signal

from src.log import logger
from src.utils import Utils
from src.xorshift import Xorshift
from src.constants import Constants as Const

__version__ = "1.0.1"


class AdvanceManager(QObject):
    """ Keeps data about current seed and advances """

    # dont use int for rng, signed int will truncate in C++ causing overflow
    # adv, tracked_rng, npc_blinks, predictions
    advance_tick = Signal(int, object, list, list)
    countdown_tick = Signal(int)              # remaining ticks
    countdown_finished = Signal(int, list)    # advances, predictions
    auto_start_countdown = Signal()           # countdown auto start

    def __init__(self):
        super().__init__()

        self._rng = None
        self._seed = None  # [s0, s1, s2, s3] as 32-bit ints

        self._min_reident = Const.DF_REIDENT_MIN_VAL
        self._max_reident = Const.DF_REIDENT_MAX_VAL

        # Advance
        self._advances = 0
        self._inc_one_on_close = True
        self._time_delay = 0.0
        self._advance_delay = 0
        self._advance_delay_2 = 0

        # Noise stuff
        self._npc_count = 0
        self._npc_pkmn_count = 0
        self._npc_phase_distance = 0  # Phase offset found during identify

        # Timeline
        self._simulating = False
        self._npc_in_timeline = 0

        # Tick rate (configurable, overridden by calibration)
        self._tick_rate = Const.FRAME_CORRECTION
        self._auto_calibrate = True

        # Tick loop thread
        self._tick_thread = None
        self._tick_running = False

        # Countdown
        self._countdown_active = False
        self._countdown_remaining = 0
        self._countdown_total = Const.DF_COUNTDOWN_DURATION_TICKS
        self._countdown_auto_start = False
        self._countdown_auto_start_adv = -1

        # Deferred advance_delay_2 (second internal countdown after main
        # countdown ends, faithful to original timeline event loop)
        self._delay2_pending = False
        self._delay2_remaining = 0

    # region Properties

    @property
    def seed(self):
        return self._seed

    @property
    def rng(self):
        return self._rng

    @property
    def inc_one_on_close(self):
        return self._inc_one_on_close

    @inc_one_on_close.setter
    def inc_one_on_close(self, value):
        self._inc_one_on_close = value

    @property
    def min_reident(self):
        return self._min_reident

    @min_reident.setter
    def min_reident(self, value):
        self._min_reident = int(value)

    @property
    def max_reident(self):
        return self._max_reident

    @max_reident.setter
    def max_reident(self, value):
        self._max_reident = int(value)

    @property
    def advances(self):
        return self._advances

    @property
    def simulating(self):
        return self._simulating

    @property
    def tracking(self):
        return self._simulating

    @property
    def time_delay(self):
        return self._time_delay

    @time_delay.setter
    def time_delay(self, value):
        self._time_delay = float(value)

    @property
    def advance_delay(self):
        return self._advance_delay

    @advance_delay.setter
    def advance_delay(self, value):
        self._advance_delay = int(value)

    @property
    def advance_delay_2(self):
        return self._advance_delay_2

    @advance_delay_2.setter
    def advance_delay_2(self, value):
        self._advance_delay_2 = int(value)

    @property
    def countdown_active(self):
        return self._countdown_active

    @property
    def countdown_total(self):
        return self._countdown_total

    @countdown_total.setter
    def countdown_total(self, value):
        self._countdown_total = int(value)

    @property
    def countdown_auto_start(self):
        return self._countdown_auto_start

    @countdown_auto_start.setter
    def countdown_auto_start(self, value):
        self._countdown_auto_start = bool(value)

    @property
    def countdown_auto_start_adv(self):
        return self._countdown_auto_start_adv

    @countdown_auto_start_adv.setter
    def countdown_auto_start_adv(self, value):
        self._countdown_auto_start_adv = int(value)

    @property
    def tick_rate(self):
        return self._tick_rate

    @tick_rate.setter
    def tick_rate(self, value):
        self._tick_rate = value

    @property
    def auto_calibrate(self):
        return self._auto_calibrate

    @auto_calibrate.setter
    def auto_calibrate(self, value):
        self._auto_calibrate = value

    @property
    def npc_count(self):
        return self._npc_count

    @npc_count.setter
    def npc_count(self, value):
        self._npc_count = int(value)

    @property
    def npc_pkmn_count(self):
        return self._npc_pkmn_count

    @npc_pkmn_count.setter
    def npc_pkmn_count(self, value):
        self._npc_pkmn_count = int(value)

    @property
    def npc_phase_distance(self):
        return self._npc_phase_distance

    @npc_phase_distance.setter
    def npc_phase_distance(self, value):
        self._npc_phase_distance = int(value)

    @property
    def npc_in_timeline(self):
        return self._npc_in_timeline

    @npc_in_timeline.setter
    def npc_in_timeline(self, value):
        self._npc_in_timeline = int(value)

    # endregion

    def is_running(self):
        return self._simulating

    def get_seed_4x32(self):
        """ Get seed as 4 hex strings of 32 bits (Chatot) """
        if self._seed is None:
            return None

        return [f"{s:08X}" for s in self._seed]

    def get_seed_2x64(self):
        """ Get seed as 2 hex strings of 64 bits (PokeFinder) """
        if self._seed is None:
            return None

        s = self._seed
        return [
            f"{s[0]:08X}{s[1]:08X}",
            f"{s[2]:08X}{s[3]:08X}",
        ]

    def set_seed(self, s0, s1, s2, s3):
        self._seed = [s0, s1, s2, s3]
        self._rng = Xorshift(s0, s1, s2, s3)
        self._advances = 1 if self._inc_one_on_close else 0
        self._simulating = False

    def start_simulating(self):
        if self._rng is None:
            return

        self._simulating = True

    def stop_simulating(self):
        self._tick_running = False
        if self._tick_thread is not None:
            self._tick_thread.join(timeout=3)
            self._tick_thread = None

        self._simulating = False
        self._countdown_active = False
        self._delay2_pending = False

    def start_countdown(self, duration_ticks=None):
        """ Start a countdown that decrements once per game tick.
        Must be called while the tick loop is running """
        if not self._tick_running:
            return

        total = duration_ticks or self._countdown_total
        self._countdown_remaining = total
        self._countdown_active = True
        logger.debug(f"[Countdown] Started: {total} ticks "
                     f"(~{total * self._tick_rate:.1f}s)")

    def stop_countdown(self):
        self._countdown_active = False
        self._countdown_remaining = 0

    def _apply_post_countdown(self):
        """ Apply post-countdown RNG advances inside the tick loop thread """
        extra = 0

        # +1 advance for game transition animation
        self._rng.next()
        extra += 1

        # +1 advance if menu close is checked
        if self._inc_one_on_close:
            self._rng.next()
            extra += 1

        # Pause the tick loop for white screen duration
        # (no RNG advances during this time, matching the game)
        if self._time_delay > 0:
            logger.debug(
                f"[Countdown] Sleeping {self._time_delay:.1f}s "
                f"(white screen transition)")
            time.sleep(self._time_delay)

        # Re-anchor timing AFTER the pause (like original:
        # waituntil = time.perf_counter())
        new_anchor = time.perf_counter()

        # Bulk advance_delay (configurable per-game scenario)
        if self._advance_delay > 0:
            self._rng.get_next_rand_sequence(self._advance_delay)
            extra += self._advance_delay
            logger.debug(
                f"[Countdown] Applying advance_delay: {self._advance_delay} "
                f"advances immediately")

        self._advances += extra

        # Schedule advance_delay_2 to fire after 10 more game ticks
        # (mirrors original: count_down resets to 10 inside event loop)
        if self._advance_delay_2 > 0:
            self._delay2_pending = True
            self._delay2_remaining = self._countdown_total
            logger.debug(
                f"[Countdown] Scheduled advance_delay_2="
                f"{self._advance_delay_2} in "
                f"{self._delay2_remaining} ticks")

        logger.debug(
            f"[Countdown] Applied post-countdown: +{extra} advances "
            f"(menu_close={self._inc_one_on_close}, "
            f"advance_delay={self._advance_delay}, "
            f"time_delay={self._time_delay:.1f}s), "
            f"total_advances={self._advances}")

        return new_anchor

    # region Tick loop

    def start_tick_loop(self, anchor):
        """ Start the dedicated advance tick thread with precise timing """
        self.stop_simulating()
        self._simulating = True
        self._tick_running = True
        self._tick_thread = Thread(
            target=self._tick_loop, args=(anchor,), daemon=True)
        self._tick_thread.start()

    def _tick_loop(self, anchor):
        """ Sleeps until exact tick boundary in a dedicated thread """
        frame_correction = self._tick_rate
        prediction_count = Const.OFFSET_ADVANCES_PREDICTION
        next_tick = anchor
        first = True

        while self._tick_running:
            now = time.perf_counter()
            sleep_time = next_tick - now
            if sleep_time > 0:
                time.sleep(sleep_time)

            tracked, npc_blinks = self.tick()
            if tracked is None:
                break

            if first:
                first = False
                tt = time.perf_counter()
                logger.debug(
                    f"[TIMING tick_loop] first_tick={tt:.3f}, "
                    f"anchor={anchor:.3f}, "
                    f"delay_from_anchor={tt - anchor:.3f}s, "
                    f"advances={self._advances}")

            predictions = self.predict_next(prediction_count)

            if (self._countdown_auto_start and
                    self._advances == self._countdown_auto_start_adv):
                logger.debug(
                    f"[Countdown] Auto-starting countdown at advance "
                    f"{self._advances} (countdown_auto_start_adv)")
                self.auto_start_countdown.emit()

            self.advance_tick.emit(
                self._advances, tracked, npc_blinks, predictions)

            # Countdown: decrement once per game tick
            if self._countdown_active:
                self._countdown_remaining -= 1
                self.countdown_tick.emit(self._countdown_remaining)

                if self._countdown_remaining <= 0:
                    self._countdown_active = False

                    # Apply all post-countdown logic in THIS thread:
                    # transition advances, time_delay pause, advance_delay,
                    # and schedule advance_delay_2
                    next_tick = self._apply_post_countdown()

                    # Emit with current state for UI rebuild
                    preds = self.predict_next(prediction_count)
                    self.countdown_finished.emit(self._advances, preds)

                    # Switch to heapq timeline if NPCs are present
                    has_timeline_npcs = (self._npc_in_timeline > 0
                                         or self._npc_pkmn_count > 0)
                    if has_timeline_npcs:
                        self._timeline_loop(next_tick, prediction_count)
                        return  # timeline_loop took over, exit tick_loop

                    continue  # skip normal next_tick increment

            # Deferred advance_delay_2: decrements after main countdown
            # ends, applies the bulk RNG jump once
            if self._delay2_pending:
                self._delay2_remaining -= 1
                if self._delay2_remaining <= 0:
                    self._delay2_pending = False
                    self._rng.get_next_rand_sequence(self._advance_delay_2)
                    self._advances += self._advance_delay_2
                    logger.debug(
                        f"[Countdown] advance_delay_2 applied: "
                        f"+{self._advance_delay_2} advances, "
                        f"total={self._advances}")

            next_tick += frame_correction

    def _timeline_loop(self, anchor, prediction_count):
        """Event-driven timeline loop using a priority queue.
        Each human NPC (+ player) blinks at fixed ~1.017s intervals.
        Each Pokemon NPC blinks at random intervals (rangefloat(3,12)+0.285).
        Each event pops from the queue, advances RNG by 1, and re-enqueues.
        """
        queue = []

        # Human NPCs + player: timeline_npc+1 entities at fixed 1.017s
        for _ in range(self._npc_in_timeline + 1):
            heapq.heappush(queue, (anchor + self._tick_rate, 0))

        # Pokemon NPCs: random interval per entity
        for _ in range(self._npc_pkmn_count):
            rand = self._rng.rangefloat(
                Const.PKMN_BLINK_INTERVAL_MIN,
                Const.PKMN_BLINK_INTERVAL_MAX) + \
                    Const.PKMN_BLINK_INTERVAL_OFFSET
            heapq.heappush(queue, (anchor + rand, 1))

        logger.debug(
            f"[Timeline] Started heapq loop: "
            f"human={self._npc_in_timeline + 1}, "
            f"pokemon={self._npc_pkmn_count}")

        delay2_countdown = self._countdown_total if self._delay2_pending \
            else -1

        while queue and self._tick_running:
            self._advances += 1

            wait, advance_type = heapq.heappop(queue)
            sleep_time = wait - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)

            # Deferred advance_delay_2 inside timeline
            if self._delay2_pending:
                if delay2_countdown > 0:
                    delay2_countdown -= 1
                elif delay2_countdown != -1:
                    delay2_countdown = -1
                    self._delay2_pending = False
                    self._rng.get_next_rand_sequence(self._advance_delay_2)
                    self._advances += self._advance_delay_2
                    logger.debug(
                        f"[Timeline] advance_delay_2 applied: "
                        f"+{self._advance_delay_2} advances, "
                        f"total={self._advances}")

            if advance_type == 0:
                # Human NPC / player blink (fixed interval)
                r = self._rng.next()
                heapq.heappush(queue, (wait + self._tick_rate, 0))
            else:
                # Pokemon NPC blink (random interval).
                # next() returns the raw 32-bit RNG; derive the float
                # interval from it the same way rangefloat() does so we
                # can emit the integer rng AND schedule the next event.
                r = self._rng.next()
                temp = (r & Const.MAX_23BIT_INT) / Const.MAX_23BIT_INT
                interval = temp * Const.PKMN_BLINK_INTERVAL_MIN + \
                    (1 - temp) * Const.PKMN_BLINK_INTERVAL_MAX + \
                    Const.PKMN_BLINK_INTERVAL_OFFSET
                heapq.heappush(queue, (wait + interval, 1))
            predictions = self.predict_next(prediction_count)
            self.advance_tick.emit(
                self._advances, r, [], predictions)

    # endregion

    def tick(self):
        """Advance 1 game frame (~1.018s).
        Returns (tracked_rng, npc_blinks):
         - tracked_rng: RNG value of the tracked entity (seq[-1])
         - npc_blinks: list of (index, is_single) for other entities
           that blinked this tick, or empty list if npc==0
        """
        if self._rng is None or not self._simulating:
            return None, []

        step = 1 + self._npc_count
        if step == 1:
            self._advances += 1
            return self._rng.next(), []

        seq = self._rng.get_next_rand_sequence(step)
        self._advances += step

        blinks = []
        for i in range(self._npc_count):
            blink_type = Utils.blink_from_rng(seq[i])
            if blink_type is not None:
                blinks.append((i, blink_type))

        return seq[-1], blinks

    def predict_next(self, count):
        """ Predict the next N advances without modifying state.
        Returns list of (advance, rng, blink_type) tuples where blink_type
        is computed from NPC[0] when NPCs exist, otherwise from the player.
        """
        if self._rng is None:
            return []

        preview = Xorshift(*self._rng.get_state())
        results = []
        adv = self._advances
        step = 1 + self._npc_count

        for _ in range(count):
            if step == 1:
                r = preview.next()
                blink = Utils.blink_from_rng(r)
            else:
                seq = preview.get_next_rand_sequence(step)
                r = seq[-1]
                blink = Utils.blink_from_rng(seq[0])
            adv += step
            results.append((adv, r, blink))

        return results

    def find_position_by_intervals(self, raw_intervals):
        """ Search for the current position in the RNG sequence
        by matching observed blink intervals against the known sequence

        Returns:
            (Xorshift, int) tuple of (rng at found position, advance index),
            or None if not found
        """
        if self._seed is None:
            return None

        intervals = raw_intervals[1:]
        search_min = self._min_reident
        search_max = self._max_reident

        if search_max < search_min:
            search_min, search_max = search_max, search_min

        observed_len = sum(intervals) + 1

        for distance in range(1 + self._npc_count):
            identify_rng = Xorshift(*self._seed)
            blinkrands = [
                (i, int((r & Const.BLINK_BIT_MASK) == 0))
                for i, r in list(enumerate(
                    identify_rng.get_next_rand_sequence(search_max)
                ))[distance::1 + self._npc_count]
            ]

            # Build sliding window of expected blink pattern
            expected_list = []
            expected = 0
            last_idx = -1
            mask = (1 << observed_len) - 1

            for idx, rand in blinkrands[:observed_len]:
                last_idx = idx
                expected = (expected << 1) | rand
            expected_list.append((last_idx, expected))

            for idx, rand in blinkrands[observed_len:]:
                last_idx = idx
                expected = ((expected << 1) | rand) & mask
                expected_list.append((last_idx, expected))

            # Build search pattern from observed intervals
            search_pattern = 1
            for i in intervals:
                search_pattern <<= i
                search_pattern |= 1

            # Search
            result_rng = Xorshift(*self._seed)
            for idx, pattern in expected_list:
                if pattern == search_pattern and search_min <= idx:
                    logger.debug(
                        f"[AdvanceManager] Found at advance:{idx}, "
                        f"distance={distance}")
                    result_rng.get_next_rand_sequence(idx)
                    return result_rng, idx

        return None

    def find_position_by_intervals_noisy(self, raw_intervals):
        """Search for the current position in the RNG sequence when a
        Pokemon NPC introduces noise (random-interval blinks) between
        the player's fixed-interval blinks.

        Uses the same algorithm as the original reidentiy_by_intervals_noisy:
        builds a boolean blink pattern from observed intervals and slides it
        over the RNG sequence, tolerating extra RNG calls from the Pokemon.

        Returns:
            (Xorshift, int) tuple of (rng at found position, advance index),
            or None if not found
        """
        if self._seed is None:
            return None

        intervals = raw_intervals[1:]
        search_min = self._min_reident
        search_max = self._max_reident

        if search_max < search_min:
            search_min, search_max = search_max, search_min

        # Build boolean blink pattern: True at blink positions
        blink_bools = [True]
        for i in intervals:
            blink_bools.extend([False] * (i - 1))
            blink_bools.append(True)
        reident_time = len(blink_bools)
        possible_length = int(reident_time * 4 // 3)

        # Pre-generate blink results for the search range
        temp_rng = Xorshift(*self._seed)
        if search_min > 0:
            temp_rng.get_next_rand_sequence(search_min)
        blink_rands = [
            int((r & Const.BLINK_BIT_MASK) == 0)
            for r in temp_rng.get_next_rand_sequence(search_max)
        ]

        # Slide the pattern and find best match (fewest pokemon insertions)
        possible_advances = []
        for advance in range(search_max - possible_length):
            blinks = blink_rands[advance:advance + possible_length]
            i = 0
            j = 0
            differences = []
            try:
                while i < reident_time:
                    diff = 0
                    while blink_bools[i] != blinks[j]:
                        diff += 1
                        j += 1
                    if diff != 0:
                        differences.append(diff)
                    j += 1
                    i += 1
            except IndexError:
                continue
            pokemon_blink_count = sum(differences)
            possible_advances.append((pokemon_blink_count, advance))

        if not possible_advances:
            return None

        best_count, best_advance = min(possible_advances)
        total_adv = search_min + best_count + best_advance + reident_time

        logger.debug(
            f"[AdvanceManager] Noisy reident found at advance: {total_adv}, "
            f"pokemon_insertions={best_count}")

        result_rng = Xorshift(*self._seed)
        result_rng.get_next_rand_sequence(total_adv)
        return result_rng, total_adv

    def reidentify(self, rng, advance):
        self._rng = rng
        self._advances = advance + (1 if self._inc_one_on_close else 0)

    def compensate_elapsed(self, offset_time, count_advances=False):
        """Advance RNG by the number of game ticks that elapsed since
        offset_time, and return a grid-aligned anchor for the tick loop.

        Args:
            offset_time: perf_counter timestamp of the last known blink
            count_advances: if True, add compensated advances to the
                counter (used by reidentify where the legacy does
                include elapsed ticks in the advance count)
        """
        now = time.perf_counter()
        if self._rng is None or offset_time is None:
            return now

        tick_rate = self._tick_rate
        elapsed = now - offset_time
        ticks = round(elapsed / tick_rate)

        if ticks > 0:
            compensated = ticks * (1 + self._npc_count)
            logger.debug(
                f"[TIMING] Compensating elapsed={elapsed:.3f}s, "
                f"ticks={ticks}, npc={self._npc_count}, "
                f"tick_rate={tick_rate:.6f}, "
                f"rng_advances={compensated}, "
                f"count={count_advances}")
            self._rng.get_next_rand_sequence(compensated)
            if count_advances:
                self._advances += compensated

        # Grid-aligned anchor: this is on the game's tick boundary
        anchor = offset_time + ticks * tick_rate
        logger.debug(
            f"[TIMING] anchor={anchor:.3f}, now={now:.3f}, "
            f"phase_correction={now - anchor:.3f}s")
        return anchor
