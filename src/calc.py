import numpy as np

from bisect import bisect
from functools import reduce

from src.constants import Constants as Const
from src.log import logger


class Calc:
    """Module for calculating Xorshift state based on observed information"""

    @staticmethod
    def pkmn_blink_interval(rng_value: int) -> float:
        """Seconds until the next Pokémon NPC blink given a raw Xorshift.

        Mirrors the game's `rangefloat(3, 12) + 0.285` derivation used by
        non-munchlax overworld Pokémon NPCs: once the state is known, every
        future blink interval is a pure function of the RNG output consumed
        by that blink event.
        """
        t = (rng_value & Const.MAX_23BIT_INT) / Const.MAX_23BIT_INT
        return (t * Const.PKMN_BLINK_INTERVAL_MIN
                + (1 - t) * Const.PKMN_BLINK_INTERVAL_MAX
                + Const.PKMN_BLINK_INTERVAL_OFFSET)

    def get_zero(self, size=32):
        """Get a matrix of the size provided filled with zeros"""
        return np.zeros((size, size), dtype="uint8")

    def get_identity(self, size=32):
        """Get an identity matrix of the size provided"""
        return np.identity(size, dtype="uint8")

    def get_shift(self, shift, size=32):
        """Get an identity matrix of the size provided shifted accordingly"""
        return np.eye(size, k=shift, dtype="uint8")

    def get_trans(self):
        """Create the transformation matrix used for Xorshift state calcs"""
        trans = np.block([
            [
                self.get_zero(), self.get_identity(),
                self.get_zero(), self.get_zero()
            ],
            [
                self.get_zero(), self.get_zero(),
                self.get_identity(), self.get_zero()
            ],
            [
                self.get_zero(), self.get_zero(),
                self.get_zero(), self.get_identity()
            ],
            [
                (self.get_identity() ^ self.get_shift(-8)
                 )@(self.get_identity() ^ self.get_shift(11)) % 2,
                self.get_zero(), self.get_zero(),
                self.get_identity() ^ self.get_shift(-19)
            ],
        ])
        return trans

    def get_ref_matrix(self, intervals, rows=33):
        """Create the matrix to be referenced for Xorshift state calculation
        based on player blink intervals.

        Each observation contributes 4 rows (bits 0..3 of the RNG output at
        that blink). For a 128-bit state the system needs rows*4 >= 128,
        i.e. rows >= 32. Default 33 yields 132 observed bits = 4 bits (1
        observation) of margin. Raise rows for more noise tolerance.
        """
        if len(intervals) < rows:
            raise ValueError(
                f"Not enough intervals for rows={rows}: "
                f"got {len(intervals)}")
        if rows * 4 < 128:
            raise ValueError(
                f"rows={rows} gives {rows*4} bits, < 128 required")

        intervals = intervals[:rows]
        base_mat = self.get_trans()
        advance_mat = self.get_trans()

        logger.debug(
            f"[Calc] get_ref_matrix rows={rows} "
            f"obs_bits={rows*4} margin_bits={rows*4 - 128} "
            f"intervals_min={min(intervals)} "
            f"intervals_max={max(intervals)} "
            f"intervals_sum={sum(intervals)}")

        ref_mat = np.zeros((4*rows, 128), "uint8")
        for i in range(rows):
            ref_mat[4*i:4*(i+1)] = base_mat[-4:]
            for _ in range(intervals[i]):
                base_mat = base_mat@advance_mat % 2
        return ref_mat

    def get_ref_matrix_munchlax(self, intervals, target_bits=144):
        """Create the matrix to be referenced for Xorshift state calculation
        based on munchlax intervals.

        Each interval contributes 4 bits when "safe" (bit 19 of rand is
        unambiguous) or 3 bits when "unsafe" (bit 19 dropped). Unsafe
        intervals used to be discarded, wasting ~44% of observations; with
        the 3-bit fallback they still contribute bits 22..20.

        Stops once total observed bits reaches target_bits (default 144 =
        128 + 16 margin, matching the original 64-blink design). Smaller
        margins (e.g. 132) were observed to leave gauss_jordan rank
        deficient on low state bits (e.g. seed_3 bit 3) that need several
        ticks of propagation to bleed into the observed bits 19..22.
        Returns (ref_mat, used_intervals) where used_intervals is a list of
        (interval_seconds, bits_used) tuples in consumption (chronological)
        order.
        """
        intervals = list(intervals[::-1])
        section = [
            0,
            3.4333333333333336, 3.795832327504833,
            3.995832327504833, 4.358332394560066,
            4.558332394560066, 4.9208324616153,
            5.120832461615299, 5.483332528670533,
            5.683332528670532, 6.045832595725767,
            6.2458325957257665, 6.608332662781,
            6.808332662780999, 7.170832729836233,
            7.370832729836232, 7.733332796891467,
            7.933332796891467, 8.2958328639467,
            8.4958328639467, 8.858332931001934,
            9.058332931001933, 9.420832998057167,
            9.620832998057166, 9.9833330651124,
            10.1833330651124, 10.545833132167635,
            10.745833132167634, 11.108333199222866,
            11.308333199222865, 11.6708332662781,
            11.8708332662781, 12.233333333333334
        ]
        base_mat = self.get_trans()
        advance_mat = self.get_trans()

        rows_list = []
        used_intervals = []
        total_bits = 0
        n_safe = 0
        n_unsafe = 0

        while intervals and total_bits < target_bits:
            value = intervals[-1]
            is_unsafe = bisect(section, value) % 2 == 1
            if is_unsafe:
                # Drop bit 19 (LSB of 4-bit extract): only rows for bits
                # 22, 21, 20.
                rows_list.append(base_mat[105:108].copy())
                bits_used = 3
                n_unsafe += 1
            else:
                rows_list.append(base_mat[105:109].copy())
                bits_used = 4
                n_safe += 1
            base_mat = base_mat @ advance_mat % 2
            intervals.pop()
            used_intervals.append((value, bits_used))
            total_bits += bits_used

        logger.debug(
            f"[Calc] munchlax get_ref_matrix consumed={len(used_intervals)} "
            f"safe={n_safe} unsafe={n_unsafe} total_bits={total_bits} "
            f"margin_bits={total_bits - 128} remaining={len(intervals)}")

        if total_bits < 128:
            raise ValueError(
                f"Insufficient bits for munchlax solve: got {total_bits}, "
                f"need >= 128. Consumed {len(used_intervals)} intervals, "
                f"{len(intervals)} left unused. Increase "
                f"BLINKS_REQUIRED_TRACKING_TIDSID")

        ref_mat = np.vstack(rows_list)
        return ref_mat, used_intervals

    def gauss_jordan(self, mat, observed: list):
        """Convert observered information and reference matrix
        to 128 bit Xorshift state via gauss jordan elimination"""
        height, width = mat.shape

        logger.debug(
            f"[Calc] gauss_jordan start mat=({height}x{width}) "
            f"observed_len={len(observed)}")

        bitmat = [self.list2bitvec(mat[i]) for i in range(height)]

        res = observed.copy()
        # forward elimination
        pivot = 0
        missing_pivots = []
        for i in range(width):
            isfound = False
            for j in range(i, height):
                if isfound:
                    check = 1 << (width-i-1)
                    if bitmat[j] & check == check:
                        bitmat[j] ^= bitmat[pivot]
                        res[j] ^= res[pivot]
                else:
                    check = 1 << (width-i-1)
                    if bitmat[j] & check == check:
                        isfound = True
                        bitmat[j], bitmat[pivot] = bitmat[pivot], bitmat[j]
                        res[j], res[pivot] = res[pivot], res[j]
            if isfound:
                pivot += 1
            else:
                missing_pivots.append(i)

        logger.debug(
            f"[Calc] gauss_jordan forward pivots_found={pivot}/{width} "
            f"missing={len(missing_pivots)}")
        if missing_pivots:
            logger.error(
                f"[Calc] gauss_jordan rank deficient: missing pivots at "
                f"columns {missing_pivots[:8]}"
                f"{'...' if len(missing_pivots) > 8 else ''} "
                f"(matrix is rank {pivot}, need {width}). "
                f"Try increasing BLINKS_REQUIRED_TRACKING")

        for i in range(width):
            check = 1 << (width-i-1)
            assert bitmat[i] & check > 0

        # backward assignment
        for i in range(1, width)[::-1]:
            check = 1 << (width-i-1)
            for j in range(i)[::-1]:
                if bitmat[j] & check == check:
                    bitmat[j] ^= bitmat[i]
                    res[j] ^= res[i]
        return res[:width]

    def bitvec2list(self, bitvec, size=128):
        """Convert bitvec of size to list of bits"""
        lst = [(bitvec >> i) & 1 for i in range(size)]
        return np.array(lst[::-1])

    def list2bitvec(self, lst):
        """Convert list of bits to bitvec"""
        bitvec = reduce(lambda p, q: (int(p) << 1) | int(q), lst)
        return bitvec

    def reverse_states(self, rawblinks: list, intervals: list) -> list:
        """Deduce state of Xorshift random number generator
        using player blinks and intervals"""
        n_blinks = len(rawblinks)
        n_intervals = len(intervals)
        n_double = sum(1 for b in rawblinks if b == 1)

        logger.debug(
            f"[Calc] reverse_states blinks={n_blinks} "
            f"intervals={n_intervals} doubles={n_double} "
            f"singles={n_blinks - n_double}")

        blinks = []
        for blink in rawblinks:
            blinks.extend([0, 0, 0])
            blinks.append(blink)

        ref_matrix = self.get_ref_matrix(intervals)
        lst_result = self.gauss_jordan(ref_matrix, blinks)
        bitvec_result = self.list2bitvec(lst_result)

        result = []
        for _ in range(4):
            result.append(bitvec_result & 0xFFFFFFFF)
            bitvec_result >>= 32

        result = result[::-1]  # reverse order
        logger.debug(
            f"[Calc] reverse_states seed=("
            f"{result[0]:#010x}, {result[1]:#010x}, "
            f"{result[2]:#010x}, {result[3]:#010x})")
        return result

    def randrange(self, rand, minimum, maximum):
        """Convert a random number into a float range"""
        rand = (rand & Const.MAX_23BIT_INT) / Const.MAX_23BIT_INT
        return rand * minimum + (1.0 - rand) * maximum

    def reverse_float_range(self, rand_float: float,
                            minimum: float, maximum: float):
        """Convert random float back to original integer"""
        norm_f = (maximum-rand_float)/(maximum-minimum)
        return int(norm_f * Const.MAX_23BIT_INT) & Const.MAX_23BIT_INT

    def reverse_states_by_munchlax(self, intervals: list) -> int:
        """Deduce state of Xorshift random number generator
        using munchlax blink intervals"""
        n_in = len(intervals)
        ref_matrix, used_intervals = self.get_ref_matrix_munchlax(intervals)

        # Build observed bit vector matching the matrix row order.
        # Matrix rows for one observation are laid out MSB-first:
        #   row 0 -> bit 22 of rand,  row 1 -> bit 21,
        #   row 2 -> bit 20,          row 3 -> bit 19 (only if safe).
        # reverse_float_range(30*f, 100, 370) >> 19 yields those 4 bits
        # with bit 3 == rand bit 22, bit 0 == rand bit 19.
        bitlst = []
        for f, bits_used in used_intervals:
            v = self.reverse_float_range(30.0 * f, 100, 370) >> 19
            bitlst.append((v >> 3) & 1)
            bitlst.append((v >> 2) & 1)
            bitlst.append((v >> 1) & 1)
            if bits_used == 4:
                bitlst.append(v & 1)

        logger.debug(
            f"[Calc] reverse_states_by_munchlax input_intervals={n_in} "
            f"used={len(used_intervals)} observed_bits={len(bitlst)} "
            f"matrix_shape={ref_matrix.shape}")

        bitvec_result = self.list2bitvec(
            self.gauss_jordan(ref_matrix, bitlst))
        result = []
        for _ in range(4):
            result.append(bitvec_result & 0xFFFFFFFF)
            bitvec_result >>= 32

        result = result[::-1]  # reverse order
        logger.debug(
            f"[Calc] reverse_states_by_munchlax seed=("
            f"{result[0]:#010x}, {result[1]:#010x}, "
            f"{result[2]:#010x}, {result[3]:#010x})")
        return result
