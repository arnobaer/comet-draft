# Devices

COMET provides a configurable generic VISA compatible device class.
Configuration is loaded from YAML files located in `comet/config/devices/<device>.yml`.

## Configuration

Devices are configured using YAML configuration files (or python dictionaries).

A simple exampel configuration defining `commands` and `sequences`.

```yaml
name: device name
commands:
  get_idn:
    method: query
    message: '*IDN?'
    require: 'INQUISITION\sINSTRUMENTS\sINC\.\,MODEL\s1250\s.*'
  get_reading:
    method: query
    message: READ?
  set_reset:
    method: write
    message: '*RST'
  set_voltage:
    method: write
    message: CTRL:VOLTS {:f}
  set_current:
    method: write
    message: CTRL:CURR {:f}
sequences:
  do_reset:
    - set_reset: []
    - set_voltage: [0]
    - set_current: [0.001]
error_parser: ERR(\d+)
error_messages:
  42: a minor error
```

### Commands

#### Getters

```yaml
commands:
  get_reading:
    method: query
    message: READ?
```

This adds a method of name `get_reading` to device using `query` as VISA method.

```python
>>> device.get_reading()
'42.123'
```

It is equivalent to the following query command.

```python
>>> device.query('READ?')
'42.123'
```

To convert the result to a type other then string, option `converter` can be used.

```yaml
commands:
  get_reading:
    method: query
    message: READ?
    converter: f
```

This tries to convert the result to `float` and raises a `DeviceError` exception
 on failure.

```python
>>> device.get_reading()
42.123
```

```yaml
commands:
  get_buffer:
    description: Retruns a numpy array containing float values
    method: query_ascii_values
    message: ':SAMP:BUFF'
    converter: f
    separator: ,
    delay: .100
```

This is equivalent to

```python
>>> device.query_ascii_values(':SAMP:BUFF', converter=f, separator=',', delay=.100)
```

#### Setters

```yaml
commands:
  set_func:
    method: write
    message: CTRL:FUNC {}
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
| `method` | VISA method used for callback |
| `message` | Message, string formatting compatible (required) |
| `choices` | List of values accepted as choices for passed arguments |
| `require` | Regular expression matching returned message |
| `converter` | Py-VISA type conversion code (s, b, c, d, o, x, e, f, g) |
| `description` | Description of the command |

```yaml
commands:
  set_func:
    method: query
    message: CTRL:FUNC {}
    choices: [ON, OFF]
    require: OK|DONE
```

```python
>>> device.set_func('ON')
'OK'
>>> device.set_func('OFF')
'OK'
>>> device.set_func(42)
Traceback (most recent call last):
  ...
DeviceError: ERROR42
```

```yaml
commands:
  set_switches:
    method: write_ascii_values
    message: CTRL:SWIT
    converter: d
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
    method: write
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

### Error handling

To handle returned error codes a regular expression can defined as `error_parser` configuration key.

```yaml
error_parser: ERR\d+
```

If a returned value matches the regular expression, a `DeviceException` is raised.

Additional error messages can be defined to match the error codes (or using a
capture group to match only a part of the error code).

```yaml
error_parser: ERR(\-?\d+)
error_messages:
  -42: "a curious error"
```

In case the device returns `ERR-42` a `DeviceException` is raised containing the message `ERR-42: a curious error`.
