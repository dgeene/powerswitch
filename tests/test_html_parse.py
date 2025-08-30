from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List
from mocks import non_wifi_homepage, wifi_homepage
from src.powerswitch.html_parser import parse_outlet_list

@dataclass
class OutletStatus:
    number: int
    name: str
    state: str

class TestHtmlParse:
    """
    The older non-wifi and newer wifi switch models have slight differences in their html
     status for the main page.
    """
    def test_wifi_html_parse(self):
        """
        Newer switch models like the LPC9 have more structured html attributes
        """
        bs = BeautifulSoup(wifi_homepage, 'html.parser')
        rows = bs.find_all('tr', class_='outlet-state-row')
        #print(rows)

        outlets: List[OutletStatus] = []

        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 3:
                number = int(cells[0].get_text(strip=True))
                name = cells[1].get_text(strip=True)
                state = cells[2].get_text(strip=True).upper()
                outlets.append(OutletStatus(number=number, name=name, state=state))
        
        print(outlets)

    def test_non_wifi_html_parse(self):
        """
        Older switch models like the LPC7 have no html attributes
        """
        print(parse_outlet_list(non_wifi_homepage))
