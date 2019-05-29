import threading
import re

from types import MethodType

class DeviceException(Exception):
    pass

class Device:
    """Generic device class.

    >>> rm = pyvisa.ResourceManager()
    >>> instr = rm.open_resource('GPIB::16')
    >>> device = Device('SMU', instr)
    >>> device.read()
    """

    RESOURCE_API = (
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

    def __init__(self, name, resource):
        self.__name = name
        self.__resource = resource
        self.__mutex = threading.Lock()
        # Create thread safe resource API
        for method in self.RESOURCE_API:
            def mutex_wrapper(callback, *args, **kwargs):
                self.__mutex.acquire()
                result = callback(*args, **kwargs)
                self.__mutex.release()
                return result
            callback = getattr(self.__resource, method)
            setattr(self, method, MethodType(mutex_wrapper, callback))

    @property
    def name(self):
        return self.__name

    @property
    def resource(self):
        return self.__resource

class DeviceFactory:
    """Device factory class.

    :param resource_manager: a VISA resource mananger instance

    >>> config = {'get_voltage': {'method': 'query', 'message': 'CTRL:VOLT?'}}
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
        device = Device(name, resource)
        for name, kwargs in config.get('routines', {}).items():
            routine = DeviceRoutine(name, **kwargs)
            if hasattr(device, routine.name):
                raise AttributeError(routine.name)
            setattr(device, routine.name, MethodType(routine, device))
        return device

class DeviceRoutine:
    """Device routine created from configuration.

    :param name: name of routine
    :param method: name of resource callback
    :param require: regular expression to validate return value (optional)
    :param description: routine documentation (optional)

    >>> routine = DeviceRoutine('set_voltage', 'query', message='CTRL:VOLT {:.6f}')
    >>> routine(device, 4.2)
    """

    def __init__(self, name, method, require=None, description=None, **kwargs):
        self.name = name
        self.method = method
        self.require = require or None
        self.description = description or ''
        self.kwargs = kwargs

    def __create_attrs(self, *args, **kwargs):
        """Create attribute set for routine call."""
        attrs = {}
        attrs.update(self.kwargs)
        if self.method in ('query', 'write'):
            attrs['message'] = attrs['message'].format(*args, **kwargs)
        elif self.method in ('query_ascii_values', 'write_ascii_values'):
            attrs['values'] = args
        elif self.method in ('query_binary_values', 'write_binary_values'):
            attrs['values'] = args
        return attrs

    def __call__(self, context, *args, **kwargs):
        attrs = self.__create_attrs(*args, **kwargs)
        result = getattr(context, self.method)(**attrs)
        # Validate return value
        if self.require is not None:
            if not re.match(self.require, result):
                raise DeviceException("invalid return value: '{result}'".format())
        return result
