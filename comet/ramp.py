import time

class Ramp:
    """Ramp iterator with integrated waiting.

    >>> ramp_up = Ramp(0, 10, step=.5, delay=0.25)
    >>> for v in ramp_up:
    ...     device.set_voltage(v)

    >>> ramp_down = Ramp(10, 0, step=-.5, delay=0.25)
    >>> for v in ramp_down:
    ...     device.set_voltage(v)

    """

    def __init__(self, start, stop, step, delay=None):
        self.start = start
        self.stop = stop
        self.step = step
        self.delay = delay or 0.0
        self.value = self.start

    def wait(self):
        time.sleep(self.delay)

    def running(self):
        if self.start >= self.stop:
            return self.value >= self.stop
        return self.value <= self.stop

    def __iter__(self):
        return self

    def __next__(self):
        self.wait()
        if self.running():
            value = self.value
            self.value = self.value + self.step
            return value
        raise StopIteration()
