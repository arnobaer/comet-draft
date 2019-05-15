import logging
import threading

from . import DeviceFactory

class DeviceAlreadyExists(Exception):
    pass

class DeviceManager:

    mutex = threading.Lock()

    def __init__(self):
        self.__factory = DeviceFactory(self.mutex)
        self.__devices = {}

    @property
    def factory(self):
        """Returns device factory instance."""
        return self.__factory

    @property
    def devices(self):
        """Retrurns devices dictionary."""
        return self.__devices

    def load(self, config):
        """Load configuration dict."""
        for device in config.get('devices'):
            self.create(device.get('name'), device)

    def create(self, name, config):
        """Create a new device from configuration dictionary."""
        if name in self.devices:
            logging.error("Device '%s' already registered", message)
            raise DeviceAlreadyExists()
        device = self.factory.create(name, config)
        self.devices[name] = device
        return device

    def get(self, name):
        """Returns device by name or None if not found."""
        return self.devices.get(name)
