import logging
from collections import OrderedDict

from .component import Component
from .metric import Metric

class Collection(Component):

    def __init__(self, app, name):
        super(Collection, self).__init__(app, name)
        self.__records = []
        self.__metrics = OrderedDict()
        self.__handles = []
        self.setup()

    @property
    def metrics(self):
        return OrderedDict(self.__metrics)

    @property
    def handles(self):
        return self.__handles

    def __len__(self):
        return len(self.__records)

    def snapshot(self, n):
        """Retruns a snapshot of recent data records."""
        return self.__records[-abs(n):]

    def snapshot_from(self, offset):
        """Retruns a snapshot of data records starting with offset."""
        return self.__records[offset:]

    def add_handle(self, handle):
        assert hasattr(handle, 'append')
        assert callable(handle.append)
        self.__handles.append(handle)
        return handle

    def add_metric(self, name, **kwargs):
        if name in self.__metrics:
            raise ValueError("Metric name already exists: '{}'".format(name))
        metric = Metric(name, **kwargs)
        self.__metrics[name] = metric
        return metric

    def setup(self):
        pass

    def configure(self):
        pass

    def append(self, **kwargs):
        logging.warning("collection[%s].append(%s)", self.name, kwargs)
        record = OrderedDict()
        for name, metric in self.__metrics.items():
            value = kwargs.get(name)
            record[name] = metric.type(value)
        self.__records.append(list(record.values()))
        for handle in self.__handles:
            handle.append(record)
