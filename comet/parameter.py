from .utilities import make_label

class Parameter:
    """Application parameter exposed in user interfaces."""

    def __init__(self, name, **kwargs):
        self.__name = name
        self.__type = kwargs.get('type', float)
        self.__value = kwargs.get('default', self.type())
        self.min = kwargs.get('min')
        self.max = kwargs.get('max')
        self.step = kwargs.get('step')
        self.prec = kwargs.get('prec')
        self.unit = kwargs.get('unit')
        self.label = kwargs.get('label', make_label(name))
        # Validate input
        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValueError("'min' argument must be less or equal (<=) 'max' argument")
        if self.prec is not None and self.type is not float:
            raise ValueError("'prec' argument is only valid for type 'float'")

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__type

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        value = self.type(value)
        if self.min and self.min > value:
            raise ValueError(value)
        if self.max and self.max < value:
            raise ValueError(value)
        self.__value = value

    def __str__(self):
        if self.prec is not None:
            return format(self.value, '.{}f'.format(self.prec))
        return format(self.value)
