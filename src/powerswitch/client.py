import requests
from requests.auth import HTTPDigestAuth
from abc import ABC, abstractmethod


class PowerSwitchClient(ABC):
    """Abstract base class for a power switch client."""

    def __init__(self, address, username, password):
        """
        Initializes the client.

        Args:
            address: The address of the power switch device.
            username: The username for authentication.
            password: The password for authentication.
        """
        self.address = address
        self.username = username
        self.password = password

    @abstractmethod
    def turn_on(self, switch_id: int):
        """Turns on a switch."""
        raise NotImplementedError

    @abstractmethod
    def turn_off(self, switch_id: int):
        """Turns off a switch."""
        raise NotImplementedError

    @abstractmethod
    def outlets(self):
        """Get all outlets."""
        raise NotImplementedError


class RestClient(PowerSwitchClient):
    """
    Controls a power switch using a REST API.
    - Turn on: POST /relay/switch/{switch_id}
    """

    def __init__(self, address, username, password):
        super().__init__(address, username, password)
        self.__session = requests.Session()
        self.__session.auth = HTTPDigestAuth(username, password)
        self.__session.headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'prefer': 'return=minimal',
            'x-csrf': 'x'}

    def turn_on(self, switch_id: int):
        """Turns on a switch."""
        res = self.__session.put(f'http://{self.address}/restapi/relay/outlets/{switch_id}/state/', json=True)
        res.raise_for_status()

    def turn_off(self, switch_id: int):
        """Turns off a switch."""
        res = self.__session.put(f'http://{self.address}/restapi/relay/outlets/{switch_id}/state/', json=False)
        res.raise_for_status()

    def outlets(self):
        """Get all outlets"""
        res = self.__session.get(f'http://{self.address}/restapi/relay/outlets/')
        res.raise_for_status()
        return res.json()


class HTTPClient(PowerSwitchClient):
    """
    Controls a power switch using simple HTTP GET requests.
    - Turn on:  GET /relay/outlet=?{switch_id}=ON
    - Turn off: GET /relay/outlet=?{switch_id}=OFF
    """
    def turn_on(self, switch_id: int):
        """Turns on a switch."""
        # Example implementation:
        # import requests
        # url = f"{self.address}/relay/outlet=?{switch_id}=ON"
        # response = requests.get(url, auth=(self.username, self.password))
        # response.raise_for_status()
        pass

    def turn_off(self, switch_id: int):
        """Turns off a switch."""
        # Example implementation:
        # import requests
        # url = f"{self.address}/relay/outlet=?{switch_id}=OFF"
        # response = requests.get(url, auth=(self.username, self.password))
        # response.raise_for_status()
        pass

    def outlets(self):
        """Get all outlets"""
        pass