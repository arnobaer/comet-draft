# Ramping

A simple way to ramp up/down voltages or other values.

```python
>>> from comet.ramp import Ramp
```

To ramp up define range, step and delay.

```python
>>> ramp_up = Ramp(start=0.0, stop=10.0, step=2.0, delay=0.25)
>>> for v in ramp_up:
...     print(v)
0
2
4
6
8
10
```

To ramp down reverse the range and step sign.

```python
>>> ramp_up = Ramp(start=10.0, stop=0.0, step=-2.0, delay=0.25)
>>> for v in ramp_up:
...     print(v)
10
8
6
4
2
0
```
