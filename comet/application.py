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
from .job import Job, JobHandle
from .service import Service
from .settings import Settings

ORG_NAME = 'HEPHY'
APP_NAME = 'comet'

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
        self.__params = OrderedDict()
        rm = pyvisa.ResourceManager(backend or self.default_backend)
        self.__manager = DeviceManager(rm)
        self.__collections = ComponentManager(self, type=Collection)
        self.__jobs = ComponentManager(self, type=Job)
        self.__services = ComponentManager(self, type=Service)
        self.__threads = []
        self.__alive = False
        self.__running = False
        self.current_job = None
        self.__mutex = threading.Lock()
        self.__asm = ApplicationStateMachine()
        self.active_jobs = set()
        self.setup()

    @property
    def name(self):
        """Retruns application name."""
        return self.__name

    @property
    def settings(self):
        """Returns dictionary of persistent application settings."""
        with Settings(ORG_NAME, APP_NAME) as settings:
            return settings

    def get(self, key, default=None):
        """Returns value by key from persistent application settings."""
        with Settings(ORG_NAME, APP_NAME) as settings:
            return settings.get(key, default)

    def set(self, key, value):
        """Set persistent application settings value for key. Value must be a JSON compatible object."""
        with Settings(ORG_NAME, APP_NAME) as settings:
            settings[key] = value

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
    def jobs(self):
        return OrderedDict([(k, JobHandle(v)) for k, v in self.__jobs.components.items()])

    def add_job(self, name, cls, *args, **kwargs):
        """Register application job.

        >>> self.add_job('my_job', MyJob)
        """
        return JobHandle(self.__jobs.add_component(cls, name, *args, **kwargs))

    @property
    def services(self):
        return self.__services.components

    def add_service(self, name, cls, *args, **kwargs):
        """Register application service.

        >>> self.add_service('my_monitor', MyMonitorService)
        """
        return self.__services.add_component(cls, name, *args, **kwargs)

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

    # states

    @property
    def is_halted(self):
        return self.__asm.is_halted

    @property
    def is_running(self):
        return self.__asm.is_running or self.__asm.is_paused

    @property
    def is_paused(self):
        return self.__asm.is_paused

    # State hooks

    def on_enter(self):
        pass

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

    def on_exit(self):
        pass

    # Controls

    def quit(self):
        """Shut down application event loop."""
        self.__alive = False

    def __configure(self):
        for collection in self.collections.values():
            collection.configure()
        for job in self.jobs.values():
            job.configure()
        for service in self.services.values():
            service.configure()

    def setup(self):
        pass

    def run(self):
        self.__alive = True
        self.__configure()

        for service in self.services.values():
            self.__threads.append(threading.Thread(target=service.run))

        for thread in self.__threads:
            thread.start()

        self.on_enter()

        # event loop
        while self.__alive:
            asm = self.__asm

            # Configure
            if asm.is_configure:
                self.__configure()

            # call state hook
            method = getattr(self, 'on_{}'.format(asm.current_state.identifier))
            method()

            # automatic transitions
            self.__mutex.acquire()
            # rRun after configure finished
            if asm.is_configure and method == self.on_configure:
                asm.run()
            # stop after running finshed
            elif asm.is_running and method == self.on_running:
                asm.stop()
            # halt after stopping finshed
            elif asm.is_stopping and method == self.on_stopping:
                asm.halt()
            self.__mutex.release()

            # throttle event loop
            time.sleep(self.event_loop_throttle)

        self.on_exit()

        for service in self.services.values():
            service.quit()

        for thread in self.__threads:
            thread.join()

        self.__threads.clear()

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
