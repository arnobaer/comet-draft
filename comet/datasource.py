import random

class DataSource:
    def __init__(self):
        self.channels = []
    def add_channel(self, source):
        self.channels.append(source)
    def read(self):
        return (source() for source in self.channels)

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
