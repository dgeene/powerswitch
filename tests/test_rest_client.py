from src.powerswitch.client import RestClient

class TestRestClient:

    def test_client_turn_on(self):
        switch = RestClient('192.168.0.100', 'admin', '1234')
        switch.turn_on(1)
