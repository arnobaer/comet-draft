import logging
import re
import threading

from types import MethodType

class DeviceException(Exception):
    pass

class DeviceAlreadyExists(DeviceException):
    pass

class DeviceManager:
    """Device manager class.

    :param resource_manager: a resource manager instance
    """

    def __init__(self, resource_manager):
        self.__factory = DeviceFactory(resource_manager)
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
        """Create devices from configuration."""
        for device in config.get('devices'):
            self.create(device.get('name'), device)

    def create(self, name, resource_name, config):
        """Create a new device from configuration."""
        if name in self.devices:
            logging.error("Device '%s' already registered", message)
            raise DeviceAlreadyExists()
        device = self.factory.create(name, resource_name, config)
        self.devices[name] = device
        return device

    def get(self, name):
        """Returns device by name or None if not found."""
        return self.devices.get(name)

class DeviceFactory:
    """Device factory class.

    :param resource_manager: a VISA resource mananger instance

    >>> config = {'commands': {'get_voltage': {'method': 'query', 'message': 'CTRL:VOLT?'}}}
    >>> factory = DeviceFactory()
    >>> device = factory.create('SMU', 'GPIB::16', config)
    >>> device.get_voltage()
    """

    def __init__(self, resource_manager):
        self.resource_manager = resource_manager

    def create(self, name, resource_name, config={}):
        """Creates a new device from configuration.

        :param name: device name
        :param resource_name: device resource name
        :param config: device configuration (optional)

        :returns: a Device instance
        """
        resource = self.resource_manager.open_resource(resource_name)
        if 'read_termination' in config:
            resource.read_termination = config.get('read_termination')
        device = Device(name, resource)
        # Create optional error handler
        if 'error_parser' in config:
            error_handler = DeviceErrorHandler(
                config.get('error_parser', r'(.*)'),
                config.get('error_messages', {})
            )
            device.append_message_handler(error_handler)
        for name, kwargs in config.get('commands', {}).items():
            command = DeviceCommand(name, **kwargs)
            if hasattr(device, command.name):
                raise AttributeError(command.name)
            setattr(device, command.name, MethodType(command, device))
        return device


class Device:
    """Generic device class.

    >>> rm = pyvisa.ResourceManager()
    >>> instr = rm.open_resource('GPIB::16')
    >>> device = Device('SMU', instr)
    >>> device.read()
    """

    ResourceAPI = (
        'query',
        'query_ascii_values',
        'query_binary_values',
        'read',
        'read_ascii_values',
        'read_binary_values',
        'write',
        'write_ascii_values',
        'write_binary_values',
    )
    """Resource methods exposed by this class."""

    def __init__(self, name, resource, message_handler=None):
        self.__name = name
        self.__resource = resource
        self.__mutex = threading.Lock()
        self.__message_handlers = []
        # Create thread safe resource API
        for method in self.ResourceAPI:
            def mutex_wrapper(callback, *args, **kwargs):
                self.__mutex.acquire()
                result = callback(*args, **kwargs)
                self.__mutex.release()
                for handler in self.__message_handlers:
                    handler.handle(result)
                return result
            callback = getattr(self.__resource, method)
            setattr(self, method, MethodType(mutex_wrapper, callback))

    @property
    def name(self):
        return self.__name

    @property
    def resource(self):
        return self.__resource

    def append_message_handler(self, handler):
        """Append a message handler instance. Resource call results are passed
        to handlers handle() mtehod.
        >>> DeviceErrorHandler(r'ERR(\d+)').handle("ERR42")
        Exception: ERR42
        """
        self.__message_handlers.append(handler)

class DeviceCommand:
    """Device command created from configuration.

    :param name: name of command
    :param method: name of resource callback
    :param require: regular expression to validate return value (optional)
    :param description: command documentation (optional)

    >>> command = DeviceCommand('set_voltage', 'query', message='CTRL:VOLT {:.6f}')
    >>> command(device, 4.2)
    """

    def __init__(self, name, method, require=None, choices=None, description=None, **kwargs):
        self.name = name
        self.method = method
        self.require = require or None
        self.choices = choices or None
        self.description = description or ''
        self.kwargs = kwargs

    def __check_choices(self, *args, **kwargs):
        if self.choices:
            for arg in args:
                if arg not in self.choices:
                    raise ValueError("invalid argument value '{}'".format(arg))
            for k, v in kwargs:
                if v not in self.choices:
                    raise ValueError("invalid argument value '{}'".format(v))

    def __create_attrs(self, *args, **kwargs):
        """Create attribute set for command call."""
        attrs = {}
        attrs.update(self.kwargs)
        if self.method in ('query', 'query_ascii_values', 'query_binary_values', 'write'):
            if 'message' not in attrs:
                raise ValueError("missing attribute 'message' for command '{}'".format(self.name))
            self.__check_choices(*args, **kwargs)
            try:
                message = attrs['message'].format(*args, **kwargs)
            except IndexError:
                raise ValueError("missing arguments for command '{}'".format(self.name))
            attrs['message'] = message
        elif self.method in ('write_ascii_values', 'write_binary_values'):
            attrs['values'] = args
        return attrs

    def __call__(self, device, *args, **kwargs):
        attrs = self.__create_attrs(*args, **kwargs)
        # Validate device method
        if self.method not in device.ResourceAPI:
            raise DeviceException("no such device method: {}".format(self.method))
        result = getattr(device, self.method)(**attrs)
        # Validate return value
        if self.require is not None:
            if not re.match(self.require, result):
                raise DeviceException("invalid return value '{}' for '{}'".format(result, self.require))
        return result

class DeviceMessageHandler:

    def handle(self, message):
        pass

class DeviceErrorHandler(DeviceMessageHandler):

    def __init__(self, expression, messages=None):
        self.parser = re.compile(expression)
        self.messages = messages or {}

    def handle(self, message):
        result = self.parser.match(format(message))
        if result:
            groups = result.groups()
            if len(groups):
                if groups[0] in self.messages:
                    raise DeviceException("{}: {}".format(message, self.messages[code]))
            raise DeviceException("{}".format(message))
