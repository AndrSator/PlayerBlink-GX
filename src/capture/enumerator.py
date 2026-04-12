from abc import ABC, abstractmethod

from src.constants import Constants as Const


class Device:
    """ Represents an input device (webcam, capture card, etc.).

    The UID is a platform-specific stable identifier (DevicePath on Windows,
    /dev/v4l/by-id entry on Linux, uniqueID on macOS). The OS index is NOT
    stored here because it can shift when devices are hot-plugged; resolve it
    just-in-time via DeviceEnumerator.resolve_index() before opening capture.
    """

    def __init__(self, uid: str, name: str):
        self._uid = uid
        self._name = name

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def name(self) -> str:
        return self._name

    def __str__(self):
        return f"{self._name} ({self._uid})"

    def __eq__(self, other):
        return isinstance(other, Device) and self._uid == other._uid

    def __hash__(self):
        return hash(self._uid)


class DeviceEnumerator(ABC):
    """ Abstract base for platform-specific video input device enumeration """

    @abstractmethod
    def list_devices(self) -> list[tuple[Device, int]]:
        """ Return a fresh list of (Device, os_index) pairs.

        os_index is the value to pass to cv2.VideoCapture() at this moment.
        Callers must not cache os_index across calls since the OS may
        reassign indices when devices are hot-plugged.
        """

    def resolve_index(self, uid: str) -> int | None:
        """ Look up the current OS index for a device by UID.

        Returns None if the device is no longer present.
        """

        for device, index in self.list_devices():
            if device.uid == uid:
                return index

        return None


def make_enumerator() -> DeviceEnumerator:
    """ Instantiate the enumerator implementation for the current platform """

    if Const.PLATFORM_WINDOWS:
        from .enumerator_win import WindowsDeviceEnumerator
        return WindowsDeviceEnumerator()

    if Const.PLATFORM_LINUX:
        from .enumerator_linux import LinuxDeviceEnumerator
        return LinuxDeviceEnumerator()

    if Const.PLATFORM_MAC:
        from .enumerator_mac import MacDeviceEnumerator
        return MacDeviceEnumerator()

    raise NotImplementedError(
        "No device enumerator available for this platform")
