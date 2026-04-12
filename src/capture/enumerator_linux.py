import os
import glob

from src.log import logger

from .enumerator import Device, DeviceEnumerator


_BY_ID_DIR = "/dev/v4l/by-id"
_V4L_SYSFS = "/sys/class/video4linux"


class LinuxDeviceEnumerator(DeviceEnumerator):
    """ Enumerates video input devices via V4L2 and sysfs.

    Primary source is /dev/v4l/by-id/, where udev creates stable symlinks
    whose names encode USB vendor/product/serial (or the USB topology path
    when no serial is available). This name is stable across disconnections
    and reboots and works as a device UID.

    Webcams often expose several video nodes per physical device (one for
    video, one for metadata). We only keep the primary capture node
    (suffix "-index0") to avoid showing duplicates.
    """

    def list_devices(self) -> list[tuple[Device, int]]:
        has_by_id = os.path.isdir(_BY_ID_DIR)
        logger.debug(
            f"[LinuxEnum] list_devices: {_BY_ID_DIR} exists={has_by_id}")

        if has_by_id:
            return self._enumerate_by_id()

        logger.debug(
            f"[LinuxEnum] {_BY_ID_DIR} not found, falling back to /dev/video*")
        return self._enumerate_fallback()

    def _enumerate_by_id(self) -> list[tuple[Device, int]]:
        devices: list[tuple[Device, int]] = []
        seen_indices: set[int] = set()

        entries = sorted(os.listdir(_BY_ID_DIR))
        logger.debug(
            f"[LinuxEnum] by-id entries ({len(entries)}): {entries}")

        for entry in entries:
            # Keep only the primary video node per physical device
            if not entry.endswith("-index0"):
                logger.debug(
                    f"[LinuxEnum] skip {entry!r} (not -index0)")
                continue

            link_path = os.path.join(_BY_ID_DIR, entry)

            try:
                target = os.path.realpath(link_path)
            except OSError as e:
                logger.warning(f"[LinuxEnum] Bad symlink {link_path}: {e}")
                continue

            logger.debug(
                f"[LinuxEnum] {entry!r} -> {target}")

            index = self._video_index_from_path(target)
            if index is None:
                logger.debug(
                    f"[LinuxEnum] skip {entry!r}: target {target!r} "
                    f"is not a /dev/videoN path")
                continue

            if index in seen_indices:
                logger.debug(
                    f"[LinuxEnum] skip {entry!r}: index {index} already seen")
                continue

            seen_indices.add(index)

            name = self._read_sysfs_name(index) or entry
            logger.debug(
                f"[LinuxEnum] + device index={index} "
                f"name={name!r} uid={entry!r}")
            devices.append((Device(uid=entry, name=name), index))

        logger.debug(
            f"[LinuxEnum] by-id enumeration produced {len(devices)} devices")
        return devices

    def _enumerate_fallback(self) -> list[tuple[Device, int]]:
        """ Use bare /dev/video* when by-id isn't available.

        No stable UID is possible here, so we use the sysfs name as a
        best-effort identifier. Devices may swap UIDs on reconnect.
        """

        devices: list[tuple[Device, int]] = []

        paths = sorted(glob.glob("/dev/video*"))
        logger.debug(f"[LinuxEnum] fallback /dev/video* paths: {paths}")

        for path in paths:
            index = self._video_index_from_path(path)
            if index is None:
                logger.debug(
                    f"[LinuxEnum] skip {path!r}: not a videoN path")
                continue

            if not self._is_capture_device(index):
                logger.debug(
                    f"[LinuxEnum] skip video{index}: not a capture device")
                continue

            name = self._read_sysfs_name(index) or f"video{index}"
            uid = f"__fallback__:{name}#{index}"
            logger.debug(
                f"[LinuxEnum] + fallback device index={index} name={name!r}")
            devices.append((Device(uid=uid, name=name), index))

        logger.debug(
            f"[LinuxEnum] fallback enum produced {len(devices)} devices")
        return devices

    @staticmethod
    def _video_index_from_path(path: str) -> int | None:
        basename = os.path.basename(path)
        if not basename.startswith("video"):
            return None
        try:
            return int(basename[len("video"):])
        except ValueError:
            return None

    @staticmethod
    def _read_sysfs_name(index: int) -> str | None:
        try:
            with open(f"{_V4L_SYSFS}/video{index}/name", "r") as f:
                return f.read().strip()
        except OSError:
            return None

    @staticmethod
    def _is_capture_device(index: int) -> bool:
        """ Check if /dev/videoN is a video capture node.

        V4L2 devices advertise their capabilities in
        /sys/class/video4linux/videoN/device_caps as a hex mask.
        Bit 0x00000001 is V4L2_CAP_VIDEO_CAPTURE.
        """

        try:
            with open(f"{_V4L_SYSFS}/video{index}/device_caps", "r") as f:
                caps = int(f.read().strip(), 16)

            return bool(caps & 0x00000001)
        except (OSError, ValueError):
            # If we can't tell, assume it's usable
            return True
