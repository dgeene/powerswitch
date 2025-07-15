import requests
from requests.auth import HTTPDigestAuth
from bs4 import BeautifulSoup
import hashlib

class TestApi:

    def test_rest_auth(self):
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'prefer': 'return=minimal',
            'x-csrf': 'x'}
        auth = HTTPDigestAuth('admin', '1234')
        res = requests.get('http://192.168.0.100/restapi/relay/', auth=auth, headers=headers)
        print('response')
        print(res.json())

    def test_http_auth(self):
        # http://192.168.0.100/index.htm # get the table with outlets status
        secure_login = False
        session = requests.Session()
        session.auth = HTTPDigestAuth('admin', '1234')
        res = session.get('http://192.168.0.100/', allow_redirects=False)
        print(res.is_redirect)
        print(res.headers)
        print(res.content)
        print(session.cookies)
        soup = BeautifulSoup(res.text, 'html.parser')
        fields = {}
        for field in soup.find_all('input'):
            name = field.get('name', None)
            value = field.get('value', '')
            if name:
                fields[name] = value
        print(fields)
        fields['Username'] = 'admin'
        fields['Password'] = '1234'
        form_response = fields['Challenge'] + fields['Username'] + fields['Password'] + fields['Challenge']
        m = hashlib.md5()
        m.update(form_response.encode())
        data = {'Username': 'admin', 'Password': m.hexdigest()}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        try:
            response = session.post('http://192.168.0.100/login.tgi', headers=headers, data=data, timeout=2.0, verify=False)
        except requests.exceptions.ConnectTimeout:
            secure_login = False
            session = None
            return
        print(session.cookies)
        if response.status_code == 200:
            if 'Set-Cookie' in response.headers:
                secure_login = True

        res2 = session.get('http://192.168.0.100/index.htm', timeout=2.0, verify=False, allow_redirects=True)
        print(res2.status_code)
        print(res2.content)

    def test_http_auth_nonwifi_switch(self):
        """
        This method of auth seems to work with non-wifi switches but not wifi switches
        """
        session = requests.Session()
        session.auth = ('admin', '1234')
        res = session.get('http://192.168.0.100/index.htm')
        print(res.content)
        assert True

