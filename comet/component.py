import time
from collections import OrderedDict

from .utilities import make_label

class BaseComponent:

    def __init__(self, app):
        super(BaseComponent, self).__init__()
        self.__app = app

    @property
    def app(self):
        """Returns application handle."""
        return self.__app

class Component(BaseComponent):
    """Application component class using name as key."""

    def __init__(self, app, name, label=None):
        super(Component, self).__init__(app)
        self.__name = name
        self.__label = label or make_label(name)

    @property
    def name(self):
        """Returns component name."""
        return self.__name

    @property
    def label(self):
        return self.__label

class ControlComponent(Component):
    """Application component with flow control functions."""

    wait_interval = 0.001

    def __init__(self, app, name, label=None):
        super(ControlComponent, self).__init__(app, name, label)

    def wait_on_pause(self):
        """Halts execution if application is paused."""
        while self.app.is_paused:
            time.sleep(self.wait_interval)

    def wait(self, delay):
        """Wait for delay in seconds.

        >>> self.wait(1.25)  # waits 1.25 seconds
        """
        t = self.time()
        while t + delay < self.time():
            time.sleep(self.wait_interval)

    def time(self):
        """Returns time in seconds.

        >>> self.time()
        1561727614.603935
        """
        return time.time()

class ComponentManager(BaseComponent):
    """Application component container storing unique, ordered components."""

    def __init__(self, app, type=None):
        super(ComponentManager, self).__init__(app)
        self.__type = type or None
        self.__components = OrderedDict()

    @property
    def components(self):
        """Returns ordered dict of components."""
        return OrderedDict(self.__components)

    def add_component(self, cls, name, *args, **kwargs):
        type_ = self.__type or Component
        if name in self.__components:
            raise ValueError("Component name for class '{}' already exists: '{}'".format(type_.__class__.__name__, name))
        component = cls(self.app, name, *args, **kwargs)
        if not isinstance(component, type_):
            raise TypeError("Component must be inherited from class '{}'".format(type_.__class__.__name__))
        self.__components[name] = component
        return component
