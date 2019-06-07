import time

class Ramp:
    """Fixed precision ramp iterator with integrated cycle delay.

    >>> ramp_up = Ramp(0, 10, step=.5, delay=0.25)
    >>> for v in ramp_up:
    ...     device.set_voltage(v)

    >>> ramp_down = Ramp(10, 0, step=-.5, delay=0.25)
    >>> for v in ramp_down:
    ...     device.set_voltage(v)

    >>> ramp = Ramp(0, 1, step=-.1, prec=1) # set fixed point precision
    >>> for v in ramp:
    ...     print(v)

    """

    DEFAULT_PREC = 9

    def __init__(self, start, stop, step, delay=None, prec=DEFAULT_PREC):
        self.prec = prec
        self.start = self._float_to_int(start)
        self.stop = self._float_to_int(stop)
        if self.start > self.stop:
            self.step = -abs(self._float_to_int(step))
        else:
            self.step = abs(self._float_to_int(step))
        if self.step == 0:
            raise ValueError("step must not be zero")
        self.value = self.start
        self.delay = float(delay)

    def wait(self):
        if self.delay:
            time.sleep(self.delay)

    @property
    def active(self):
        if self.start == self.stop:
            return False
        if self.start >= self.stop:
            return self.value >= self.stop
        return self.value <= self.stop

    def _float_to_int(self, value):
        return int(round(value * 10**self.prec))

    def _int_to_float(self, value):
        return value / 10**self.prec

    def __iter__(self):
        return self

    def __next__(self):
        # wait only between steps
        start, stop = sorted((self.start, self.stop))
        if start < self.value <= stop:
            self.wait()
        if self.active:
            value = self._int_to_float(self.value)
            self.value = self.value + self.step
            return value
        raise StopIteration()
