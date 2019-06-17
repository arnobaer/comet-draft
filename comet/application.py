import time
import logging
import threading
from collections import OrderedDict

import pyvisa

from .device import DeviceManager
from .parameter import Parameter
from .collection import Collection
from .procedure import Procedure

class Application:
    """Base class for comet applications.

    :name: the application's name
    :backend: PyVisa backend (optional, default is '@py')
    """

    default_backend = '@py'

    def __init__(self, name, backend=None):
        self.__name = name
        self.__attrs = OrderedDict()
        self.__params = OrderedDict()
        rm = pyvisa.ResourceManager(backend or self.default_backend)
        self.__manager = DeviceManager(rm)
        self.__collections = OrderedDict()
        self.__procedures = OrderedDict()
        self.__alive = False
        self.__running = False

    @property
    def name(self):
        """Retruns application name."""
        return self.__name

    @property
    def attrs(self):
        return self.__attrs

    def get(self, key, default=None):
        """Returns application attribute."""
        return self.__attrs.get(key, default)

    def set(self, key, value):
        """Set application attribute."""
        self.__attrs[key] = value

    @property
    def params(self):
        return self.__params

    def register_param(self, name, **kwargs):
        """Register application parameter."""
        if name in self.__params:
            raise KeyError("Parameter with name '{}' already registered.".format(name))
        param = Parameter(name, **kwargs)
        self.__params[name] = param
        return param

    @property
    def manager(self):
        return self.__manager

    @property
    def devices(self):
        return self.__manager.devices

    def register_device(self, name, resource_name, **kwargs):
        """Register device."""
        if name in self.__manager.devices:
            raise KeyError("Device with name '{}' already registered.".format(name))
        device = self.__manager.create(name, resource_name, **kwargs)
        return device

    @property
    def collections(self):
        return self.__collections

    def register_collection(self, name, cls, *args, **kwargs):
        """Register data collection.

        >>> self.register_collection('my_coll', MyCollection)
        """
        if name in self.__collections:
            raise KeyError("Collection with name '{}' already registered.".format(name))
        collection = cls(self, name, *args, **kwargs)
        if not isinstance(collection, Collection):
            raise TypeError("Collection type must be inherited from class {}".format(Collection.__class__.__name__))
        self.__collections[name] = collection
        return collection

    @property
    def procedures(self):
        return self.__procedures

    def register_procedure(self, name, cls, *args, **kwargs):
        """Register operation procedure.

        >>> self.register_procedure('my_proc', MyProcedure)
        """
        if name in self.__procedures:
            raise KeyError("Procedure with name '{}' already registered.".format(name))
        procedure = cls(self, name, *args, **kwargs)
        if not isinstance(procedure, Procedure):
            raise TypeError("Procedure type must be inherited from class {}".format(Procedure.__class__.__name__))
        self.__procedures[name] = procedure
        return procedure

    @property
    def running(self):
        """Returns True if application is running."""
        return self.__running

    def start(self):
        """Start application run."""
        self.__running = True

    def stop(self):
        """Stop application run."""
        self.__running = False

    def shutdown(self):
        self.stop()
        self.__alive = False

    def run(self):
        self.__alive = True
        for collection in self.collections.values():
            collection.setup()
        for procedure in self.procedures.values():
            procedure.setup()
        threads = []
        while self.__alive:
            # Run procedure stack or default empty behaviour
            if self.procedures:
                for procedure in self.procedures.values():
                    if not procedure.continious:
                        procedure.run()
            else:
                time.sleep(1)
                logging.warning(time.time())
                logging.warning("running: %s", self.__running)
        for thread in threads:
            thread.join()
