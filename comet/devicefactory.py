from . import Driver
from . import Device

from types import MethodType

class DeviceFactory:

    def __init__(self, mutex):
        self.mutex = mutex

    def register_method(self, device, method, name, command):
        """Registers get/set methods loaded from config."""
        def wrapper(self, *args, **kwargs):
            logging.debug("%s(%s)::%s(command='%s')", self.__class__.__name__, device, name, command)
            return method(command.format(*args, **kwargs))
        setattr(device, name, MethodType(wrapper, device))

    def create(self, name, config):
        driver = Driver(
            resource=config.get('resource', 'GPIB0::10::INSTR'),
            backend=config.get('backend', '@sim'),
        )
        device = Device(driver, self.mutex, config)
        # Register methods from configuration
        for key, value in config.get('commands', {}).items():
            # Register query command
            if re.match(r'^get_\w+$', key):
                self.register_method(device, device.query, key, value)
            # Register write command
            if re.match(r'^set_\w+$', key):
                self.register_method(device, device.write, key, value)
        return device

if __name__ == '__main__':
    import doctest
    doctest.testmod()
