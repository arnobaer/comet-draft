import time

class Ramp:
    """Fixed precision ramp iterator with integrated cycle delay.

    >>> ramp_up = Ramp(0, 10, step=.5, delay=0.25)
    >>> for v in ramp_up:
    ...     device.set_voltage(v)

    >>> ramp_down = Ramp(10, 0, step=-.5, delay=0.25)
    >>> for v in ramp_down:
    ...     device.set_voltage(v)

    >>> ramp = Ramp(0, 1, step=.001, prec=3) # set fixed point precision
    >>> for v in ramp:
    ...     device.set_voltage(v)

    Every iteration is delayed with exception of first and last iteration.

    Ramp(0,3,1): [0]<--delay-->[1]<--delay-->[2]<--delay-->[3]

    """

    DEFAULT_PREC = 6

    def __init__(self, start, stop, step, delay=0, prec=DEFAULT_PREC):
        start = round(start * 10**prec)
        stop = round(stop * 10**prec)
        step = round(step * 10**prec)
        stop += step
        self.__range = range(start, stop, step)
        self.__prec = prec
        self.delay = delay
        self.reset()

    def reset(self):
        """Reset range iterator."""
        self.__iter = self.__range.__iter__()

    def wait(self):
        """Delay method, overwrite for custom implementation."""
        time.sleep(self.delay)

    @property
    def start(self):
        return self.__range.start / 10**self.__prec

    @property
    def stop(self):
        return (self.__range.stop - self.__range.step) / 10**self.__prec

    @property
    def step(self):
        return self.__range.step / 10**self.__prec

    def __iter__(self):
        return self

    def __next__(self):
        try:
            value = next(self.__iter)
            # Delay only iterations within range
            start, stop = sorted((self.__range.start, self.__range.stop))
            if start < value < stop:
                self.wait()
            return value / 10**self.__prec
        except StopIteration:
            self.reset()
            raise
