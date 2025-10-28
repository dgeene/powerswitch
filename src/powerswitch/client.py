import hashlib
import socket
import requests
import paramiko
from bs4 import BeautifulSoup
from requests.auth import HTTPDigestAuth
from abc import ABC, abstractmethod
from .html_parser import parse_outlet_list


class SSHProxy:
    """SSH tunnel proxy for requests library."""

    def __init__(self, proxy_config):
        self.proxy_config = proxy_config
        self.ssh_client = None
        self.local_port = None

    def __enter__(self):
        # Create SSH client
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to SSH server
        self.ssh_client.connect(
            self.proxy_config["host"],
            port=self.proxy_config.get("port", 22),
            username=self.proxy_config["username"],
            password=self.proxy_config["password"],
        )

        # Find an available local port
        sock = socket.socket()
        sock.bind(("", 0))
        self.local_port = sock.getsockname()[1]
        sock.close()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ssh_client:
            self.ssh_client.close()

    def get_proxy_url(self, target_host):
        """Start port forwarding and return proxy URL."""
        try:
            # Setup remote port forwarding
            self.ssh_client.get_transport().request_port_forward(
                "127.0.0.1",
                self.local_port,
                target_host,
                80,  # Assuming HTTP port
            )
            return f"http://127.0.0.1:{self.local_port}"
        except Exception as e:
            raise RuntimeError(f"Failed to setup SSH tunnel: {str(e)}")


class PowerSwitchClient(ABC):
    """Abstract base class for a power switch client."""

    def __init__(self, address, username, password, proxy_config=None):
        """
        Initializes the client.

        Args:
            address: The address of the power switch device.
            username: The username for authentication.
            password: The password for authentication.
            proxy_config: Optional SSH proxy configuration dictionary with keys:
                         host, port (optional), username, password
        """
        self.address = address
        self.username = username
        self.password = password
        self.proxy_config = proxy_config
        self._proxy = None

    def _get_base_url(self):
        """Get the base URL, considering proxy if configured."""
        if self.proxy_config and not self._proxy:
            self._proxy = SSHProxy(self.proxy_config)
            self._proxy.__enter__()
            return self._proxy.get_proxy_url(self.address)
        return f"http://{self.address}"

    def __del__(self):
        """Cleanup proxy if used."""
        if self._proxy:
            self._proxy.__exit__(None, None, None)

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
            "accept": "application/json",
            "content-type": "application/json",
            "prefer": "return=minimal",
            "x-csrf": "x",
        }

    def turn_on(self, switch_id: int):
        """Turns on a switch."""
        base_url = self._get_base_url()
        res = self.__session.put(
            f"{base_url}/restapi/relay/outlets/{switch_id}/state/", json=True
        )
        res.raise_for_status()

    def turn_off(self, switch_id: int):
        """Turns off a switch."""
        base_url = self._get_base_url()
        res = self.__session.put(
            f"{base_url}/restapi/relay/outlets/{switch_id}/state/", json=False
        )
        res.raise_for_status()

    def outlets(self):
        """Get all outlets"""
        base_url = self._get_base_url()
        res = self.__session.get(f"{base_url}/restapi/relay/outlets/")
        res.raise_for_status()
        return res.json()


class HTTPClient(PowerSwitchClient):
    """
    Controls a power switch using simple HTTP GET requests.
    - Turn on:  GET /relay/outlet=?{switch_id}=ON
    - Turn off: GET /relay/outlet=?{switch_id}=OFF
    """

    def __init__(self, address, username, password):
        super().__init__(address, username, password)
        self.secure_login = False
        self.__session = requests.Session()
        self.__session.auth = HTTPDigestAuth(username, password)
        self.__authenticate()

    def __authenticate(self):
        base_url = self._get_base_url()
        res = self.__session.get(f"{base_url}/", allow_redirects=False)
        soup = BeautifulSoup(res.text, "html.parser")
        fields = {}
        for field in soup.find_all("input"):
            name = field.get("name", None)
            value = field.get("value", "")
            if name:
                fields[name] = value

        fields["Username"] = self.username
        fields["Password"] = self.password
        form_response = (
            fields["Challenge"]
            + fields["Username"]
            + fields["Password"]
            + fields["Challenge"]
        )
        m = hashlib.md5()
        m.update(form_response.encode())
        data = {"Username": self.username, "Password": m.hexdigest()}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            response = self.__session.post(
                f"{base_url}/login.tgi",
                headers=headers,
                data=data,
                timeout=2.0,
                verify=False,
            )
        except requests.exceptions.ConnectTimeout:
            self.secure_login = False
            self.__session = None
            return

        if response.status_code == 200:
            if "Set-Cookie" in response.headers:
                self.secure_login = True

    def turn_on(self, switch_id: int):
        """Turns on a switch."""
        base_url = self._get_base_url()
        res = self.__session.get(f"{base_url}/outlet?{switch_id}=ON")
        res.raise_for_status()

    def turn_off(self, switch_id: int):
        """Turns off a switch."""
        base_url = self._get_base_url()
        res = self.__session.get(f"{base_url}/outlet?{switch_id}=OFF")
        res.raise_for_status()

    def outlets(self):
        """Get all outlets"""
        base_url = self._get_base_url()
        res = self.__session.get(
            f"{base_url}/index.htm", timeout=2.0, verify=False, allow_redirects=True
        )
        res.raise_for_status()
        return parse_outlet_list(res.text)
