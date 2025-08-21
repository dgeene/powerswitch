from src.powerswitch.client import RestClient, HTTPClient

class TestRestClient:

    def test_client_turn_on(self):
        switch = RestClient('192.168.0.100', 'admin', '1234')
        switch.turn_on(1)
        print(switch.outlets())

class TestHttpClient:

    def test_client_turn_on(self):
        switch = HTTPClient('192.168.0.100', 'admin', '1234')
        print(switch.outlets())
