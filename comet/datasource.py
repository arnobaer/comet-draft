import random
import threading

class DataSource:

    def __init__(self):
        self.channels = []
        self.handlers = []
        self.mutex = threading.Lock()
    def add_channel(self, source):
        self.channels.append(source)
    def add_handler(self, handler):
        self.handlers.append(handler)
    def read(self):
        self.mutex.acquire()
        data = tuple(source() for source in self.channels)
        for handler in self.handlers:
            handler.append(data)
        self.mutex.release()
        return data

class FakeDataChannel:
    def __init__(self, value, minimum, maximum, gain, var):
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.gain = gain
        self.var = var
    def reset(self):
        self.value = self.minimum
        self.gain = abs(self.gain)
    def next(self):
        self.value += random.uniform(*self.var) * self.gain
        if self.value >= self.maximum:
            self.gain = -self.gain
        if self.value <= self.minimum:
            self.gain = -self.gain
        return self.value

class FakeDataSource(DataSource):
    def __init__(self):
        super(FakeDataSource, self).__init__()
        self.source_a = FakeDataChannel(0., 0., 1., +1., (.002, .03))
        self.source_b = FakeDataChannel(0.5, 0., 1., +1., (.001, .05))
        self.add_channel(random.random)
        self.add_channel(lambda: random.uniform(.1,.5))
        self.add_channel(self.source_a.next)
        self.add_channel(self.source_b.next)
    def reset_a(self):
        self.source_a.reset()
    def reset_b(self):
        self.source_b.reset()
    def gain(self):
        for _ in range(8):
            self.source_a.next()
            self.source_b.next()
