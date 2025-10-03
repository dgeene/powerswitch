# ⚡ Powerswitch ⚡

Yet another web power switch library for the Digital Loggers Web Power Switch

- It needs to have a cli client and a module to be used by scripts.
- The cli client needs to handle multiple switches through a configuration.
- It needs to handle the rest api of the newer wifi switches.
- It needs to handle the older http only switches. All transparently.

## Getting Started

Using the powerswitch client.


### Installing the CLI tool
TBD


## Development

Building documentation

### Testing
Setting up a configuration. To work with multiple switches create a `.config` directory with `switches.json`.

The idea with the named outlets is to quickly provide the cli with outlet names. This would have to be synchronized with what is actually configured in the switch.

To test against multiple switches populate the json file like so:
```json
[
  {
    "name": "PS1",
    "host": "10.0.0.100",
    "username": "admin",
    "password": "1234",
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
    "outlets": {

    }
  },
]
```

You can then specify which switch to test against when running pytest with `--cfg=PS2`


#### Testing the cli without installing

To test the cli without pipx install just run it as a module (from the project root): `python -m src.powerswitch.cli`

## Resources

Rest API guide with examples: https://www.digital-loggers.com/rest.html

Rest API with very comprehensive model object reference: https://public.digital-loggers.com/docs/branches/h215c0b26f88abacd8baef9182dcef80946a551dd/object_model_reference/refman.pdf

