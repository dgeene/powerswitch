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


class RestClient(PowerSwitchClient):
    """
    Controls a power switch using a REST API.
    - Turn on: POST /relay/switch/{switch_id}
    """
    def turn_on(self, switch_id: int):
        """Turns on a switch."""
        # Example implementation:
        # import requests
        # url = f"{self.address}/relay/switch/{switch_id}"
        # response = requests.post(url, auth=(self.username, self.password))
        # response.raise_for_status()
        pass

    def turn_off(self, switch_id: int):
        """Turns off a switch."""
        # The user did not specify how to turn off a switch with the REST API.
        # This could be a DELETE request, or a POST with a different body/endpoint.
        # Example with DELETE:
        # import requests
        # url = f"{self.address}/relay/switch/{switch_id}"
        # response = requests.delete(url, auth=(self.username, self.password))
        # response.raise_for_status()
        pass


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