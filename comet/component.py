from collections import OrderedDict

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

    def __init__(self, app, name):
        super(Component, self).__init__(app)
        self.__name = name

    @property
    def name(self):
        """Returns component name."""
        return self.__name

class ComponentManager(BaseComponent):
    """Application component container storing unique, ordered components."""

    def __init__(self, app):
        super(ComponentManager, self).__init__(app)
        self.__components = OrderedDict()

    @property
    def components(self):
        """Returns ordered dict of components."""
        return OrderedDict(self.__components)

    def add_component(self, cls, name, *args, **kwargs):
        if name in self.__components:
            raise ValueError("Component name already exists: '{}'".format(name))
        component = cls(self.app, name, *args, **kwargs)
        if not isinstance(component, Component):
            raise TypeError("Component must be inherited from class {}".format(Component.__class__.__name__))
        self.__components[name] = component
        return component
