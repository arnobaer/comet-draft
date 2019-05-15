import logging
import threading

from . import DeviceFactory

class DeviceAlreadyExists(Exception):
    pass

class DeviceManager:

    mutex = threading.Lock()

    def __init__(self):
        self.__factory = DeviceFactory()
        self.__devices = {}

    @property
    def factory(self):
        return self.__factory

    @property
    def devices(self):
        return self.__devices

    def create(self, name, config):
        """Create a new device from configuration dictionary."""
        if name in self.devices:
            logging.error("Device '%s' already registered", message)
            raise DeviceAlreadyExists()
        self.devices[name] = self.factory.create(self.mutex, name, config)

    def get(self, name):
        return self.devices.get()
