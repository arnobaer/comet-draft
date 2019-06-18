from .utilities import make_label

class Parameter:
    """Application parameter exposed in user interfaces."""

    numeric_types = [int, float]

    def __init__(self, name, **kwargs):
        self.__name = name
        self.__type = kwargs.get('type', float)
        self.__value = kwargs.get('default', self.type())
        self.min = kwargs.get('min')
        self.max = kwargs.get('max')
        self.prec = kwargs.get('prec')
        self.step = kwargs.get('step')
        self.unit = kwargs.get('unit')
        self.required = kwargs.get('required') or False
        self.label = kwargs.get('label', make_label(name))
        # Calculate step for a given precision
        if self.prec is not None and self.step is None:
            self.step = 1./10**self.prec
        # Validate input
        if self.min is not None and self.max is not None and self.min > self.max:
            raise ValueError("'min' argument must be less or equal (<=) 'max' argument")
        if self.prec is not None and self.type is not float:
            raise ValueError("'prec' argument is only valid for type 'float'")

    @property
    def name(self):
        """Returns parameter name."""
        return self.__name

    @property
    def type(self):
        """Retruns parameter type."""
        return self.__type

    @property
    def is_numeric(self):
        """Retruns True if parameter type is numeric (int, float) else False."""
        return self.type in self.numeric_types

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
