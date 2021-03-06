import re

class VariantError(Exception):
    pass

class Variant:
    """Generic value container providing methods to manipulate and convert a value.
    """

    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @property
    def type(self):
        """Retruns type of value.
        >>> Variant(42).type
        <class 'int'>
        >>> Variant('0x2a').type
        <class 'str'>
        """
        return type(self.__value)

    def __len__(self):
        return len(self.__value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            self.__value == other.value
        return self.__value == other

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            self.__value < other.value
        return self.__value < other

    def to(self, type, *args, **kwargs):
        """Convert value to type. Any type, function or class can be
        passed as type argument. Returns a Variant object so method can
        be changed to continue conversion to another type if required.

        >>> value = Variant('0x2a')
        >>> value.to(int, 16)
        42
        >>> value.to(int, 16).to(float)
        42.0
        """
        try:
            return Variant(type(self.__value, *args, **kwargs))
        except Exception as e:
            raise VariantError(e)

    def toint(self, base=None):
        if base is not None:
            return self.to(int, base=base)
        return self.to(int)

    def __int__(self):
        try:
            return int(self.__value)
        except Exception as e:
            raise VariantError(e)

    def tofloat(self):
        return self.to(float)

    def __float__(self):
        try:
            return float(self.__value)
        except Exception as e:
            raise VariantError(e)

    def tostr(self):
        return self.to(str)

    def __str__(self):
        try:
            return str(self.__value)
        except Exception as e:
            raise VariantError(e)

    def tobytes(self):
        return self.encode()

    def __bytes__(self):
        return self.encode()

    def encode(self, *args, **kwargs):
        """Encode string value to bytes. Returns Variant value."""
        try:
            return Variant(self.__value.encode(*args, **kwargs))
        except Exception as e:
            raise VariantError(e)

    def decode(self, *args, **kwargs):
        """Decode bytes value to string. Returns Variant value."""
        try:
            return Variant(self.__value.decode(*args, **kwargs))
        except Exception as e:
            raise VariantError(e)

    def format(self, *args, **kwargs):
        """String format value using builtin function format."""
        try:
            return format(self.__value, *args, **kwargs)
        except Exception as e:
            raise VariantError(e)

    def __repr__(self):
        return self.__value.__repr__()

    def strip(self, *args, **kwargs):
        """Strip string representation, returns stripped Variant value."""
        try:
            return Variant(self.__value.strip(*args, **kwarg))
        except Exception as e:
            raise VariantError(e)

    def split(self, pattern=None, **kwargs):
        """Use regular expression split method to extract a value from string
        representation. If no pattern is given it performs a regular string
        split. Returns list of Variant values.

        >>> value = Variant('42, 43, 44')
        >>> value.split(',')
        ['42', ' 43', ' 44']
        >>> value.split(r'\s*,\s*')
        ['42', '43', '44']
        >>> value.split()
        ['42,', '43,', '44']
        """
        if pattern is None:
            try:
                return self.__value.split(**kwargs)
            except Exception as e:
                raise VariantError(e)
        try:
            values = re.split(pattern, self.__value, **kwargs)
        except Exception as e:
            raise VariantError(e)
        return [Variant(value) for value in values]

    def search(self, pattern, **kwargs):
        """Use regular expression search method to extract a value from string
        representation. Returns tuple of Variant values or None if not found.

        >>> value = Variant('int spam=42;')
        >>> value.search(r'(\d+);')
        ['42', '43', '44']
        """
        result = re.search(pattern, self.__value, **kwargs)
        if result is not None:
            try:
                return tuple([Variant(value) for value in result.groups()])
            except Exception as e:
                raise VariantError(e)


    def findall(self, pattern, **kwargs):
        """Use regular expression findall method to extract values from string
        representation. Returns list of Variant values or list of tuples of
        Variant values (depending on capturing parantesis) or an empty list if
        not found.

        >>> value = Variant('42, 43, 44,')
        >>> value.findall(r'\d+')
        ['42', '43', '44']

        >>> value = Variant('4:01, 4:02, 4:03,')
        >>> value.findall(findall(r'(\d+):(\d+)')
        [['4', '01'], ['4', '02'], ['4', '03']]
        """
        try:
            results = re.findall(pattern, self.__value, **kwargs)
        except Exception as e:
            raise VariantError(e)
        if results and isinstance(results[0], str):
            return [Variant(value) for value in results]
        return [tuple([Variant(value) for value in values]) for values in results]
