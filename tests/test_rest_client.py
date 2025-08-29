from src.powerswitch.client import RestClient, HTTPClient

class TestRestClient:

    def test_client_turn_on(self, acct):
        switch = RestClient(acct.host, acct.username, acct.password)
        switch.turn_on(1)
        print(switch.outlets())

class TestHttpClient:

    def test_client_turn_on(self, acct):
        switch = HTTPClient(acct.host, acct.username, acct.password)
        print(switch.outlets())
