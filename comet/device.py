import logging
import time
import re

from types import MethodType

from . import Driver

class Device:
    """Generic configurable VISA device."""

    default_config = {
        'get_idn': '*IDN?',
        'set_reset': '*rst',
        'set_clear': '*cls',
    }
    """Default VISA resource configuration, can be overwritten by user configuration."""

    throttle = 0.05
    """Throttle for executing list of reset commands, in seconds."""

    def __init__(self, driver, mutex, config=None):
        self.__driver = driver
        self.__mutex = mutex
        # Copy default configuration
        self.__config = self.default_config.copy()
        # Update configuration
        if config is not None:
            self.__config.update(config)
        # Register methods from configuration
        for key, value in self.__config.items():
            # Register query command
            if re.match(r'^query_\w+$', key):
                self.__register(self.query, key, value)
            # Register write command
            if re.match(r'^write_\w+$', key):
                self.__register(self.write, key, value)
            # Register read command
            if re.match(r'^read_\w+$', key):
                self.__register(self.read, key, None)

    def __register(self, method, name, command):
        """Registers get/set methods loaded from config."""
        def wrapper(self, *args, **kwargs):
            logging.debug("%s(%s)::%s(command='%s')", self.__class__.__name__, self.resource, name, command)
            return method(command.format(*args, **kwargs))
        setattr(self, name, MethodType(wrapper, self))

    @property
    def driver(self):
        """Returns device driver."""
        return self.__driver

    @property
    def config(self):
        """Returns device configuration dictionary."""
        return self.__config

    @property
    def resource(self):
        """Returns VISA resource from configuration."""
        return self.config.get('Visa_Resource')

    def read(self):
        """Read from VISA resource. Use optional type callback to cast result."""
        logging.debug("%s(%s)::read()", self.__class__.__name__, self.resource)
        return self.driver.read(self.resource)

    def write(self, command):
        """Write to from VISA resource."""
        logging.debug("%s(%s)::write(command='%s')", self.__class__.__name__, self.resource, command)
        self.driver.write(self.resource, command)

    def query(self, command):
        """Query from VISA resource. Use optional type callback to cast result."""
        logging.debug("%s(%s)::query(command='%s')", self.__class__.__name__, self.resource, command)
        return self.driver.query(self.resource, command)

    def reset(self):
        commands = self.config.get('reset')
        if commands is None:
            return
        for command in commands:
            for k, v in command.items():
                k = 'set_{}'.format(k)
                getattr(self, k)(v)
                # HACK self.read() # free buffer -- Ugh! Some instruments might require this!
                time.sleep(self.throttle)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
