from . import Driver
from . import Device

class DeviceFactory:

    def __init__(self):
        pass

    def create(self, mutex, name, config):
        driver = Driver(
            resource=config.get('resource', 'GPIB0::10::INSTR'),
            backend=config.get('backend', '@sim'),
        )
        device = Device(driver, mutex)
        return device
