import re

class Value:
    """Generic value container providing methods to manipulate and convert a value."""
    
    def __init__(self, value):
        self.__value = value

    @property
    def type(self):
        """Retruns type of value.
        >>> Value(42).type
        <class 'int'>
        >>> Value('0x2a').type
        <class 'str'>
        """
        return type(self.__value)

    def convert(self, type, *args, **kwargs):
        """Convert value to type. Any type, function or class can be
        passed as type argument. Returns a Value object so method can
        be changed to continue conversion to another type if required.
        
        >>> value = Value('0x2a')
        >>> value.convert(int, 16)
        42
        >>> value.convert(int, 16).convert(float)
        42.0
        """
        return Value(type(self.__value, *args, **kwargs))

    @property
    def str(self):
        return str(self.__value)

    def __str__(self):
        return self.str

    def __repr__(self):
        return format(self.__value)

    @property
    def int(self):
        return int(self.__value)

    def __int__(self):
        return self.int

    @property
    def float(self):
        return float(self.__value)

    def __float__(self):
        return self.float
    
    def split(self, sep=None, maxsplit=-1):
        values = self.str.split(sep, maxsplit)
        if type is not None:
            return [Value(value) for value in values]
        return values
    
    def findall(self, pattern, flags=0):
        results = re.findall(pattern, self.str, flags)
        return [[Value(value) for value in values] for values in results]
