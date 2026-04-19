from comtypes import COMError, GUID, client
from comtypes.persist import IPropertyBag

from pygrabber.dshow_core import ICreateDevEnum
from pygrabber.dshow_ids import DeviceCategories, clsids

from src.log import logger

from .enumerator import Device, DeviceEnumerator


class WindowsDeviceEnumerator(DeviceEnumerator):
    """ Enumerates video input devices via DirectShow.

    Uses the moniker property bag to read both FriendlyName and DevicePath.
    DevicePath is a stable per-USB-port identifier that survives device
    disconnection and reshuffling — we use it as the Device UID so that the
    application can distinguish between physically different webcams even if
    they share the same friendly name.
    """

    def list_devices(self) -> list[tuple[Device, int]]:
        devices: list[tuple[Device, int]] = []

        try:
            system_device_enum = client.CreateObject(
                clsids.CLSID_SystemDeviceEnum, interface=ICreateDevEnum)
            filter_enum = system_device_enum.CreateClassEnumerator(
                GUID(DeviceCategories.VideoInputDevice), dwFlags=0)
        except (COMError, OSError) as e:
            logger.error(f"[WinEnum] Failed to create device enumerator: {e}")
            return devices

        if filter_enum is None:
            # No video input devices available
            return devices

        index = 0

        try:
            moniker, count = filter_enum.Next(1)
        except ValueError:
            return devices

        while count > 0:
            try:
                prop_bag = moniker.BindToStorage(
                    0, 0, IPropertyBag._iid_).QueryInterface(IPropertyBag)

                name = prop_bag.Read("FriendlyName", pErrorLog=None)

                try:
                    device_path = prop_bag.Read("DevicePath", pErrorLog=None)
                except COMError:
                    # Some virtual devices do not expose DevicePath
                    device_path = None

                uid = device_path or f"__noDevPath__:{name}#{index}"
                devices.append((Device(uid=uid, name=name), index))
            except COMError as e:
                logger.warning(
                    f"[WinEnum] Could not read device at index {index}: {e}")

            index += 1

            try:
                moniker, count = filter_enum.Next(1)
            except ValueError:
                break

        return devices
