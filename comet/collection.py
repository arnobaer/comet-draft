import logging

from collections import OrderedDict
from .utilities import make_label

class Collection:

    def __init__(self, app, name):
        self.__app = app
        self.__name = name
        self.data = []
        self.metrics = OrderedDict()
        self.handles = []

    @property
    def app(self):
        return self.__app

    @property
    def name(self):
        return self.__name

    def register_handle(self, handle):
        assert hasattr(handle, 'append')
        assert callable(handle.append)
        self.handles.append(handle)

    def register_metric(self, name, **kwargs):
        assert name not in self.metrics
        metric = Metric(name, **kwargs)
        self.metrics[name] = metric
        return metric

    def setup(self):
        pass

    def append(self, **kwargs):
        logging.warning("collection[%s].append(%s)", self.name, kwargs)
        values = OrderedDict()
        for name, metric in self.metrics.items():
            value = kwargs.get(name)
            values[name] = metric.type(value)
        self.data.append(list(values.values()))
        for handle in self.handles:
            handle.append(values)

class Metric:

    def __init__(self, name, **kwargs):
        self.name = name
        self.type = kwargs.get('type', float)
        self.unit = kwargs.get('unit', None)
        self.label = kwargs.get('label', make_label(name))
