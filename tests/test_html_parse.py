from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List
from mocks import non_wifi_homepage, wifi_homepage

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
        bs = BeautifulSoup(non_wifi_homepage, 'html.parser')
        target_table = None

        for table in bs.find_all('table'):
            if table.find(string=lambda text: text and "Individual Control" in text):
                target_table = table
                break
        print(target_table)
        outlets: List[OutletStatus] = []

        if target_table:
            for row in target_table.find_all('tr', attrs={"bgcolor": "#F4F4F4"}):
                cells = row.find_all('td')
                if len(cells) >= 3:
                    number = int(cells[0].get_text(strip=True))
                    name = cells[1].get_text(strip=True)
                    state = cells[2].get_text(strip=True).upper()
                    outlets.append(OutletStatus(number, name, state))
        print(outlets)
