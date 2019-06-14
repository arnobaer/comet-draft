from collections import OrderedDict

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
        self.__backend = backend or self.default_backend
        self.__attrs = OrderedDict()
        self.__params = OrderedDict()
        self.__collections = OrderedDict()
        self.__procedures = OrderedDict()
        self.__alive = False
        self.__running = False

    @property
    def name(self):
        """Retruns application name."""
        return self.__name

    @property
    def backend(self):
        """Returns application PyVisa backend."""
        return self.__backend

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
    def collections(self):
        return self.__collections

    def register_collection(self, name, cls, *args, **kwargs):
        """Register data collection."""
        if name in self.__collections:
            raise KeyError("Collection with name '{}' already registered.".format(name))
        collection = cls(name, *args, **kwargs)
        if not isinstance(collection, Collection):
            raise TypeError("Collection type must be inherited from class {}".format(Collection.__class__.__name__))
        self.__collections[name] = collection
        return collection

    @property
    def procedures(self):
        return self.__procedures

    def register_procedure(self, name, cls, *args, **kwargs):
        """Register operation procedure."""
        if name in self.__procedures:
            raise KeyError("Procedure with name '{}' already registered.".format(name))
        procedure = cls(name, *args, **kwargs)
        if not isinstance(procedure, Procedure):
            raise TypeError("Procedure type must be inherited from class {}".format(Procedure.__class__.__name__))
        self.__procedures[name] = procedure
        return procedure

    @property
    def running(self):
        return self.__running

    def start(self):
        self.__running = True

    def stop(self):
        self.__running = False

    def shutdown(self):
        self.__alive = False

    def run(self):
        self.__alive = True
        for collection in self.collections.values():
            collection.setup()
        for procedure in self.procedures.values():
            procedure.setup()
        import time, logging
        while self.__alive:
            time.sleep(1)
            logging.warning(time.time())
            logging.warning("running: %s", self.__running)


class Parameter:
    """Application parameter exposed in user interfaces."""

    def __init__(self, name, **kwargs):
        self.name = name
        self.type = kwargs.get('type', float)
        self.value = kwargs.get('default', self.type())
        self.prec = kwargs.get('prec', 3)
        self.unit = kwargs.get('unit')
        self.label = kwargs.get('label', self.name.capitalize().replace('_', ' '))
