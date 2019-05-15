# Data handlers

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
>>> datasource.read()
# writes to file 'dump.dat':
# 't=1557748564.916\t0.9\t0.2\tchoice='8'\n'
```
