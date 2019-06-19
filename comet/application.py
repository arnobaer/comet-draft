import time
import logging
import threading
from collections import OrderedDict

import pyvisa

from .device import DeviceManager
from .parameter import Parameter
from .collection import Collection
from .state import State

class StopException(Exception):
    pass

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
        self.__states = OrderedDict()
        self.__monitoring = OrderedDict()
        self.__alive = False
        self.__running = False
        self.current_state = None

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
    def states(self):
        return self.__states

    def register_state(self, name, cls, *args, **kwargs):
        """Register operation state.

        >>> self.register_state('my_proc', MyState)
        """
        if name in self.__states:
            raise KeyError("State with name '{}' already registered.".format(name))
        state = cls(self, name, *args, **kwargs)
        if not isinstance(state, State):
            raise TypeError("State type must be inherited from class {}".format(State.__class__.__name__))
        self.__states[name] = state
        return state

    @property
    def monitoring(self):
        return self.__monitoring

    def register_monitoring(self, name, cls, *args, **kwargs):
        """Register continious monitoring operations.

        >>> self.register_monitoring('my_mon', MyMonitoring)
        """
        if name in self.__monitoring:
            raise KeyError("Monitoring with name '{}' already registered.".format(name))
        monitor = cls(self, name, *args, **kwargs)
        if not isinstance(monitor, State):
            raise TypeError("Monitoring type must be inherited from class {}".format(State.__class__.__name__))
        self.__monitoring[name] = monitor
        return monitor

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

    def setup(self):
        for collection in self.collections.values():
            collection.setup()
        for state in self.states.values():
            state.setup()
        for monitor in self.monitoring.values():
            monitor.setup()

    def create_threads(self):
        threads = []
        for monitor in self.monitoring.values():
            def wrapper():
                while self.__alive:
                    monitor.run()
            thread = threading.Thread(target=wrapper)
            threads.append(thread)
        return threads

    def run(self):
        self.__alive = True
        self.setup()
        threads = self.create_threads()
        for thread in threads:
            thread.start()
        while self.__alive:
            if self.running:
                # Run state stack or default empty behaviour
                if self.states:
                    for state in self.states.values():
                        self.current_state = state.name
                        logging.warning("running state: %s", state.name)
                        state.progress = 0
                        p = threading.Thread(target=state.run)
                        logging.warning("state[%s][starting][progress %.3f%%]", state.name, state.progress)
                        p.start()
                        while p.is_alive():
                            logging.warning("state[%s][running][progress %.2f%%]", state.name, state.progress)
                            time.sleep(.25)
                        p.join()
                        logging.warning("state[%s][done][progress %.2f%%]", state.name, state.progress)
                        if state.progress == 0:
                            state.progress = 100
                else:
                    time.sleep(1)
                    logging.warning(time.time())
                    logging.warning("running: %s", self.running)
                self.__running = False
                self.current_state = None
        for thread in threads:
            thread.join()
