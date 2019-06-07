# Ramping

A simple way to ramp up/down voltages or other values in fixed precision.

Default precision is 9.

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

To ramp down just reverse the range, the proper sign of the step is calculated.

```python
>>> ramp_down = Ramp(start=10.0, stop=0.0, step=2.0, delay=0.25)
>>> for v in ramp_down:
...     print(v)
10
8
6
4
2
0
```

To ramp using a certain precision use the `prec` argument. Values are rounded.

```python
>>> ramp = Ramp(start=0.0, stop=1.0, step=0.25, prec=1)
>>> for v in ramp_down:
...     print(v)
0.0
0.2
0.4
0.6
0.8
1.0
```
