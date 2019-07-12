import logging
import re
import threading
from collections import OrderedDict

from pyvisa import util as pyvisa_util

from types import MethodType

from .variant import Variant

class DeviceException(Exception):
    pass

class DeviceFactory:
    """Device factory class.

    :param resource_manager: a VISA resource mananger instance

    >>> config = {'commands': {'get_voltage': {'method': 'query', 'message': 'CTRL:VOLT?'}}}
    >>> factory = DeviceFactory()
    >>> device = factory.create('SMU', 'GPIB::16', config)
    >>> device.get_voltage()
    """

    resource_options = (
        'CR',
        'LF',
        'chunk_size',
        'encoding',
        'query_delay',
        'read_termination',
        'timeout',
        'write_termination',
    )
    """Resource specific config options."""

    def __init__(self, resource_manager):
        self.resource_manager = resource_manager

    def create(self, name, resource_name, config={}):
        """Creates a new device from configuration.

        :param name: device name
        :param resource_name: device resource name
        :param config: device configuration (optional)

        :returns: a Device instance
        """
        options = {}
        for key in self.resource_options:
            if key in config:
                options[key] = config.get(key)
        resource = self.resource_manager.open_resource(resource_name, **options)
        device = Device(name, resource)
        # Config values
        setattr(device, 'model', config.get('name'))
        # Create optional error handler
        if 'errors' in config:
            messages = config.get('errors').get('messages', {})
            expression = config.get('errors').get('expression')
            if expression is not None:
                error_handler = DeviceErrorHandler(expression, messages)
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
    >>> device.query('*IDN?')
    'INQUISITION INSTRUMENTS INC.,MODEL 1250'
    """

    def __init__(self, name, resource):
        self.__name = name
        self.__resource = resource
        self.__mutex = threading.Lock()
        self.__message_handlers = []

    @property
    def name(self):
        return self.__name

    @property
    def resource(self):
        return self.__resource

    @property
    def mutex(self):
        return self.__mutex

    def query(self, message, *args, **kwargs):
        """A combination of write(message) and read()."""
        with self.mutex:
            result = self.resource.query(message, *args, **kwargs)
            for handler in self.__message_handlers:
                handler.handle(result)
            return Variant(result)

    def read(self, *args, **kwargs):
        """Read a string from the device."""
        with self.mutex:
            result = self.resource.read(*args, **kwargs)
            for handler in self.__message_handlers:
                handler.handle(result)
            return Variant(result)

    def read_raw(self, *args, **kwargs):
        """Read the unmodified string sent from the instrument to the computer."""
        with self.mutex:
            result = self.resource.read_raw(*args, **kwargs)
            for handler in self.__message_handlers:
                handler.handle(result)
            return Variant(result)

    def read_bytes(self, count, *args, **kwargs):
        """Read a certain number of bytes from the instrument."""
        with self.mutex:
            result = self.resource.read_bytes(count, *args, **kwargs)
            for handler in self.__message_handlers:
                handler.handle(result)
            return Variant(result)

    def write(self, message, *args, **kwargs):
        """Write a string message to the device."""
        with self.mutex:
            return self.resource.write(message, *args, **kwargs)

    def write_raw(self, message):
        """Write a message as byte to the device."""
        with self.mutex:
            return self.resource.write_raw(message)

    def query_bytes(self, message, count, *args, **kwargs):
        """Returns decoded byte string by writing raw query message.

        >>> device.query_bytes(b'T', 13)
        'T120619130943'
        """
        with self.mutex:
            self.resource.write_raw(message)
            result = self.resource.read_bytes(count, *args, **kwargs)
            for handler in self.__message_handlers:
                handler.handle(result)
            return Variant(result)

    def append_message_handler(self, handler):
        """Append a message handler instance. Resource call results are passed
        to handlers handle() method.
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
        if self.require is not None:
            self.require = re.compile(self.require)

    @property
    def __name__(self):
        return self.name

    @property
    def __doc__(self):
        return "{}".format(self.description)

    def __validate_choices(self, *args, **kwargs):
        if self.choices is None:
            return
        for arg in args:
            if arg not in self.choices:
                raise ValueError("invalid argument value '{}'".format(arg))
        for k, v in kwargs:
            if v not in self.choices:
                raise ValueError("invalid argument value '{}'".format(v))

    def __create_attrs(self, *args, **kwargs):
        """Create attributes for command call."""
        attrs = {}
        # Load defaults
        attrs.update(self.kwargs)
        # Parse string formatting in message
        if self.method in ('query', 'write'):
            if 'message' not in attrs:
                raise ValueError("missing attribute 'message' for command '{}'".format(self.name))
            self.__validate_choices(*args, **kwargs)
            try:
                message = attrs.get('message').format(*args, **kwargs)
            except IndexError:
                raise ValueError("missing arguments for command '{}'".format(self.name))
            attrs['message'] = message
        return attrs

    def __call__(self, device, *args, **kwargs):
        attrs = self.__create_attrs(*args, **kwargs)
        # Validate device method
        if not hasattr(device, self.method):
            raise DeviceException("no such device method: {}".format(self.method))
        result = getattr(device, self.method)(**attrs)
        # Validate return value
        if self.require is not None:
            if not self.require.match(result.str):
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
        """Handle device message, raises a DeviceException if message matches
        error expression."""
        result = self.parser.match(format(message))
        if result:
            groups = result.groups()
            if len(groups):
                key = groups[0]
                if key in self.messages:
                    raise DeviceException("{}: {}".format(message, self.messages[key]))
            raise DeviceException("{}".format(message))
