# Data sources

Create a custom data source by inheriting class `comet.DataSource` and assign functors to data channels.

```python
from comet.datasource import DataSource

class MyDataSource(DataSource):
    def __init__(self):
        super(DataSource, self).__init__()
        # Add data channel callbacks providing data
        self.add_channel(time.time)
        self.add_channel(random.random)
        self.add_channel(lambda: random.uniform(.1, .2))
        self.add_channel(self.read_channel)
    def read_channel(self):
        return random.choice((2, 4, 6, 8))
```
Calling method `read()` will return a data sample

```python
>>> datasource.read()
(1557748564.916238, 0.9003779309695682, 0.15396819823042876, 8)
```
