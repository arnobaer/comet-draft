# Settings

Stores persistent application settings in JSON format using class `Settings`.

Used as context manager it takes care of creating a configuration file in the
platform specific location dedicated for user configurations.

## Examples

To access application specific settings the organization and application names
are required. All alterations of dictionary `settings` are written to file when
exiting the `with` block.

```python
import comet

with comet.Settings('HEPHY', 'comet') as settings:
    if 'user' not in settings:
        settings['user'] = "Monty"
    name = settings.get('user')
```

To access settings read-only set argument `persistent` to `False`.

```python
import comet

with comet.Settings('HEPHY', 'comet', persistent=False) as settings:
    name = settings.get('user')
```
