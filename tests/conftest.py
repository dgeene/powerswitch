import json
import pytest
from pathlib import Path
from dataclasses import dataclass

here = Path(__file__).resolve().parent
root = here.parent
config_path = root / '.config' / 'switches.json'


def pytest_addoption(parser):
    parser.addoption(
        "--cfg", action="store", default="PS7", help="The switch name from config.json"
    )

@dataclass
class ConnInfo:
    name: str
    host: str
    username: str
    password: str

@pytest.fixture
def acct(request):
    credentials = request.config.getoption("--cfg")
    with open(config_path) as f:
        config = json.load(f)
        for c in config:
            if c['name'] == credentials:
                return ConnInfo(**c)
    raise ValueError(f"No configuration found for switch name: {credentials}")

