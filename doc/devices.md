# Devices

COMET provides a configurable generic VISA compatible device class.
Configuration is loaded from YAML files located in `comet/config/devices/<device>.yml`.

## Configuration

Devices are configured using YAML configuration files (or python dictionaries).

A simple exampel configuration defining `commands` and `sequences`.

```yaml
name: device name
commands:
  get_idn: '*IDN?'
  get_reading: READ?
  set_reset: '*RST'
  set_voltage: CTRL:VOLTS {:f}
  set_current: CTRL:CURR {:f}
sequences:
  call_reset:
    - set_reset: []
    - set_voltage: [0]
    - set_current: [0.001]
```

### Commands

#### Getters

```yaml
commands:
  get_reading: READ?
```

This adds a method of name `get_reading` to device using `query` as default method.

```python
>>> device.get_reading()
'42.123'
```

It is equivalent to the following query command.

```python
>>> device.query('READ?')
'42.123'
```

To convert the result to a type other then string, option `type` can be used.

```yaml
commands:
  get_reading:
    message: READ?
    type: float
```

This tries to convert the result to `float` and raises a `DeviceError` exception on failure.

```python
>>> device.get_reading()
42.123
```

```yaml
commands:
  get_buffer:
    escription: Retruns a numpy array containing float values
    method: query_ascii_values
    message: ':SAMP:BUFF'
    convert: float
    separator: ,
    container: tuple
    delay: .100
```

This is equivalent to

```python
>>> device.query_ascii_values(':SAMP:BUFF', convert=float, separator=',', container=tuple, delay=.100)
```

#### Setters

```yaml
commands:
  set_func: CTRL:FUNC {}
```

```python
>>> device.set_func('ON')
True
```

is equivalent to

```python
>>> device.write('CTRL:FUNC ON')
True
```

More options

| Option | Description |
| --- | --- |
| `message` | Message, string formatting compatible (required) |
| `method` | VISA method (optional, default is `write` for commands beginning with `set_*` and `query` for methods beginning with `get_*`) |
| `success` | Regular expression matching returned message (optional, sets `method` to `query` if not set) |
| `failure` | Regular expression to parse errors if `success` did not match (optional). |

```yaml
commands:
  set_func:
    method: query
    message: CTRL:FUNC {}
    choices: [ON, OFF]
    success: OK|DONE
    failure: Err(\d+)
```

```python
>>> device.set_func('ON')
'OK'
>>> device.set_func('OFF')
'OK'
>>> device.set_func(42)
Traceback (most recent call last):
  ...
DeviceError: Err42
```

```yaml
commands:
  set_switches:
    method: write_ascii_values
    message: CTRL:SWIT
    converter: int
```

```python
>>> switches = (2, 4, 7)
>>> device.set_switches(*switches)
True
```

This is equivalent to

```yaml
commands:
  set_switches:
    message: CTRL:SWIT {}
```

```python
>>> switches = (2, 4, 7)
>>> device.set_switches(','.join(map(str, switches)))
True
```

### Sequences

Sequences are lists of commands executed in order, sequences names must start with `do_*`.

```yaml
sequences:
  do_reset:
    - set_reset: []
    - set_voltage: [0]
    - set_current: [0.001]
    - set_switches: [2, 4, 7]
```

```python
>>> device.do_reset()
```

This is equivalent to

```python
>>> device.set_reset()
>>> device.set_voltage(0)
>>> device.set_current(0.001)
>>> device.set_switches(2, 4, 7)
```