from .utilities import make_label

class Metric:

    def __init__(self, name, **kwargs):
        self.__name = name
        self.__type = kwargs.get('type', float)
        self.__unit = kwargs.get('unit', None)
        self.__label = kwargs.get('label', make_label(name))

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def unit(self):
        return self.__unit

    @property
    def label(self):
        return self.__label
