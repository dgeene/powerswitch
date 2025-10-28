# ⚡ Powerswitch ⚡

Yet another web power switch library for the Digital Loggers Web Power Switch

- It needs to have a cli client and a module to be used by scripts.
- The cli client needs to handle multiple switches through a configuration.
- It needs to handle the rest api of the newer wifi switches.
- It needs to handle the older http only switches. All transparently.

## Getting Started

### Using the CLI

Setting up a configuration. To work with multiple switches create a `$HOME/.config/powerswitch` directory with `switches.json`.

Use this as a template:
```json
[
  {
    "name": "PS1",
    "host": "10.0.0.100",
    "username": "admin",
    "password": "1234",
    "restapi": true,
    "cycletime": 5,
    "outlets": {
      "1": "eth switch",
      "2": "fan",
      "3": "weatherstation",
      "4": "lights"
    }
  },
  {
    "name": "PS2",
    "host": "10.0.0.101",
    "username": "admin",
    "password": "1234",
    "restapi": true,
    "cycletime": 5,
    "outlets": {

    }
  },
]
```

Notable settings. restapi=true if the switch model supports the rest api. the fallback is to use webpage processing. cycletime is the delay between cycling a switch from on -> and vice versa.

### Using the powerswitch client classes.

```python
from powerswitch.client import RestClient, HTTPClient

switch = RestClient(hostname, username, password)
switch.turn_on(1)
```


### Installing the CLI tool
TBD


## Development

Setup for development: `poetry install --with dev`

Autoformatting: `poetry run ruff format <file>`

Building documentation

### Testing

The idea with the named outlets is to quickly provide the cli with outlet names. This would have to be synchronized with what is actually configured in the switch.



#### Testing the cli without installing

To test the cli without pipx install just run it as a module (from the project root): `python -m src.powerswitch.cli PS7 1 on`

Outlet names can also be used from the config file: ``python -m src.powerswitch.cli PS7 fan on`

## Resources

Rest API guide with examples: https://www.digital-loggers.com/rest.html

Rest API with very comprehensive model object reference: https://public.digital-loggers.com/docs/branches/h215c0b26f88abacd8baef9182dcef80946a551dd/object_model_reference/refman.pdf

