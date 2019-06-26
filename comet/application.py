import time
import logging
import threading
from collections import OrderedDict

from statemachine import StateMachine, State
import pyvisa

from .parameter import Parameter
from .device import DeviceManager
from .component import ComponentManager
from .collection import Collection
from .procedure import Procedure

class Application:
    """Base class for comet applications.

    :name: the application's name
    :backend: PyVisa backend (optional, default is '@py')
    """

    default_backend = '@py'

    event_loop_throttle = .25
    """Throttles event loop on repeating states."""

    def __init__(self, name, backend=None):
        self.__name = name
        self.__attrs = OrderedDict()
        self.__params = OrderedDict()
        rm = pyvisa.ResourceManager(backend or self.default_backend)
        self.__manager = DeviceManager(rm)
        self.__collections = ComponentManager(self)
        self.__procedures = ComponentManager(self)
        self.__processes = ComponentManager(self)
        self.__alive = False
        self.__running = False
        self.current_procedure = None

        self.__mutex = threading.Lock()
        self.__asm = ApplicationStateMachine()

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

    def add_param(self, name, **kwargs):
        """Register application parameter."""
        if name in self.__params:
            raise KeyError("Parameter with name '{}' already registered.".format(name))
        param = Parameter(name, **kwargs)
        self.__params[name] = param
        return param

    # Components

    @property
    def devices(self):
        return self.__manager.devices

    def add_device(self, name, resource_name, **kwargs):
        """Register device."""
        if name in self.__manager.devices:
            raise KeyError("Device with name '{}' already registered.".format(name))
        device = self.__manager.create(name, resource_name, **kwargs)
        return device

    @property
    def collections(self):
        return self.__collections.components

    def add_collection(self, name, cls, *args, **kwargs):
        """Register data collection.

        >>> self.add_collection('my_coll', MyCollection)
        """
        return self.__collections.add_component(cls, name, *args, **kwargs)


    @property
    def procedures(self):
        return self.__procedures.components

    def add_procedure(self, name, cls, *args, **kwargs):
        """Register operation procedure.

        >>> self.add_procedure('my_proc', MyProcedure)
        """
        return self.__procedures.add_component(cls, name, *args, **kwargs)

    @property
    def processes(self):
        return self.__processes.components

    def add_process(self, name, cls, *args, **kwargs):
        """Register continious process operations.

        >>> self.add_process('my_mon', MyMonitoring)
        """
        return self.__processes.add_component(cls, name, *args, **kwargs)

    @property
    def state(self):
        """Returns application state."""
        return self.__asm.current_state.name

    # Commands

    def start(self):
        """Start application run."""
        self.__mutex.acquire()
        if self.__asm.is_halted:
            self.__asm.start()
        self.__mutex.release()

    def stop(self):
        """Stop application run."""
        self.__mutex.acquire()
        if self.__asm.is_running or self.__asm.is_paused:
            self.__asm.stop()
        self.__mutex.release()

    def pause(self):
        """Pause running application."""
        self.__mutex.acquire()
        if self.__asm.is_running:
            self.__asm.pause()
        self.__mutex.release()

    def unpause(self):
        """Continues paused application."""
        self.__mutex.acquire()
        if self.__asm.is_paused:
            self.__asm.unpause()
        self.__mutex.release()

    # State hooks

    def on_halted(self):
        pass

    def on_configure(self):
        pass

    def on_running(self):
        pass

    def on_pause(self):
        pass

    def on_stopping(self):
        pass

    # Controls

    def quit(self):
        """Shut down application event loop."""
        self.__alive = False

    def __configure(self):
        for collection in self.collections.values():
            collection.configure()
        for procedure in self.procedures.values():
            procedure.configure()
        for monitor in self.processes.values():
            monitor.configure()

    def run(self):
        self.__alive = True
        self.__configure()

        threads = []
        for process in self.processes.values():
            threads.append(threading.Thread(target=process.run))

        for thread in threads:
            thread.start()

        # event loop
        while self.__alive:
            # call state hook
            method = 'on_{}'.format(self.__asm.current_state.identifier)
            if hasattr(self, method):
                getattr(self, method)()
            # automatic transitions
            self.__mutex.acquire()
            asm = self.__asm
            if asm.is_configure:
                asm.run()
            elif asm.is_running:
                asm.stop()
            elif asm.is_stopping:
                asm.halt()
            self.__mutex.release()
            # throttle event loop
            time.sleep(self.event_loop_throttle)

        for process in self.processes.values():
            process.quit()

        for thread in threads:
            thread.join()

class ApplicationStateMachine(StateMachine):
    """Application state machine."""

    halted = State('Halted', initial=True)
    configure = State('Configure')
    running = State('Running')
    paused = State('Paused')
    stopping = State('Stopping')

    start = halted.to(configure)
    run = configure.to(running)
    pause = running.to(paused)
    unpause = paused.to(running)
    stop = running.to(stopping) | paused.to(stopping)
    halt = stopping.to(halted)
