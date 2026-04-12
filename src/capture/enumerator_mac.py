from .enumerator import Device, DeviceEnumerator


class MacDeviceEnumerator(DeviceEnumerator):

    def list_devices(self) -> list[tuple[Device, int]]:
        raise NotImplementedError(
            "macOS device enumeration is not implemented yet")

    def resolve_index(self, uid: str) -> int | None:
        raise NotImplementedError(
            "macOS device enumeration is not implemented yet")
