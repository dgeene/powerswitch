from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List

@dataclass
class OutletStatus:
    number: int
    name: str
    state: str


def parse_outlet_list(html):
    """
    Parse outlet list for the non wifi switch like the LPC7
    """
    bs = BeautifulSoup(html, 'html.parser')
    outlets: List[OutletStatus] = []
    target_table = None

    for table in bs.find_all('table'):
        if table.find(string=lambda text: text and "Individual Control" in text):
            target_table = table
            break

    if target_table:
        for row in target_table.find_all('tr', attrs={"bgcolor": "#F4F4F4"}):
            cells = row.find_all('td')
            if len(cells) >= 3:
                number = int(cells[0].get_text(strip=True))
                name = cells[1].get_text(strip=True)
                state = cells[2].get_text(strip=True).upper()
                outlets.append(OutletStatus(number, name, state))
    return outlets
