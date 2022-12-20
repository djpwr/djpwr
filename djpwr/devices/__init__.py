"""
from djpwr.devices import dev, DeviceRegistry

dev['users'] = get_manager('users.User)
dev['replacements'] = get_manager('replacements.Replacement')


mgrs = DeviceRegistry()

mgrs['users'] = get_manager('users.User')
mgrs['replacements'] = get_manager('replacements.Replacement')


replacement = mgrs['replacements'].by_id(replacement_id)


for user in mgrs['users'].recently_active():
    pass

"""


class DeviceRegistry(object):
    class MissingDevice(KeyError):
        pass

    def __init__(self):
        self._devices = {}

    def register(self, device_name, value, allow_override=False):
        existing, override_existing = self._get_device(device_name)

        if existing != self.MissingDevice and not override_existing:
            raise RuntimeError("Device already registered", device_name)

        self._devices[device_name] = (value, allow_override)

    def _get_device(self, device_name):
        return self._devices.get(device_name, (self.MissingDevice, True))

    def __getitem__(self, device_name):
        device, _ = self._get_device(device_name)

        if device == self.MissingDevice:
            raise self.MissingDevice("Device not registered", device_name)

        return device

    def __setitem__(self, device_name, value):
        existing, _ = self._get_device(device_name)

        if existing != self.MissingDevice:
            raise RuntimeError("Device already registered", device_name)

        self._devices[device_name] = (value, False)

    def register_manager(self, device_name, manager_attr='objects'):
        def model_class_wrapper(model_class):
            self[device_name] = getattr(model_class, manager_attr)

            return model_class

        return model_class_wrapper


dev = DeviceRegistry()
