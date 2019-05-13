# COMET

## Quickstart

Running the technical demonstrator

    $ pip install -r requirements.txt
    $ python -m comet.main --port 8080

Use your web browser to access http://localhost:8080/

## Data sources

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

## Data writer

Writing acquired data directly to a file by inheriting from class `DataWriter` and overloading method `format`. Class `DataSource` supports multiple data handlers to be assigned.

```python
from comet.datawriter import DataWriter

class MyDataWriter(DataWriter):
    def format(self, data):
        """My custom data format for assigned data source."""
        return "t={0:.3f}, {1:.1f}, {2:.1f}, choice='{3}'))".format(data=data)

handler = DataWriter('dump.dat')
datasource.add_handler(handler)
```

Reading from a data source triggers all assigned data handlers.

```python
datasource.read()
# writes following line to file 'dump.dat'
# 't=1557748564.916\t0.9\t0.2\tchoice='8'\n'
```
