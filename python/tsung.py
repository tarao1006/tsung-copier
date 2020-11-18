"""
Requirement
-----------
- python >= 3.8 (due to the walrus operator)
- beautifulsoup4
- requests

Examples
--------
>>> python tsung.py -w -u http://localhost:8000/report.html
"""
import argparse
import dataclasses
from typing import List

import bs4
import requests
from bs4 import BeautifulSoup


# 欲しい情報はここで制限できる
IDS = [
    'stats',
    'transaction',
    'network',
    'count',
    'errors',
    'os_mon',
    'http_status',
]


class StatsTable:
    def __init__(self):
        self.values = []

    def __repr__(self):
        return f'{[value for value in self.header]}\n{[value for value in self.values]}'

    def set_header(self, elements: bs4.ResultSet) -> None:
        self.header = self.formater(elements)

    def add_values(self, elements: bs4.ResultSet) -> None:
        self.values.append(self.formater(elements))

    def print_table(self):
        header = '|'
        header += '|'.join(self.header)
        header += '|\n'
        for i in range(len(self.header)):
            header += '|:-:'
        header += '|\n'

        values = ''
        for value in self.values:
            values += '|'
            values += '|'.join(value)
            values += '|\n'
        print(header + values)

    def formater(self, elements: bs4.ResultSet) -> List[str]:
        return [element.text.strip().replace('\n', '') for element in elements]

    def print_rate(self) -> None:
        results = {}
        for value in self.values:
            for i, data in enumerate(value):
                if i == 0:
                    status = int(data)
                elif i == 1:
                    hightest_rate = float(data.split(' ')[0])
                elif i == 2:
                    mean_rate = float(data.split(' ')[0])
                elif i == 3:
                    total_number = int(data)
            results[status] = Result(status, hightest_rate, mean_rate, total_number)

        total = 0
        total_2xx = 0
        total_5xx = 0

        for key, value in results.items():
            total += value.total_number
            if str(key).startswith('2'):
                total_2xx += value.total_number
            elif str(key).startswith('5'):
                total_5xx += value.total_number

        if total_5xx != 0:
            rate = f'{total_2xx / total_5xx:.2f}'
        else:
            rate = '-'

        print('## Calculated Values\n|Topic|Value|\n|:-:|:-:|')
        print(f'|total_2xx|{total_2xx:.0f}|\n|total_5xx|{total_5xx:.0f}|')
        print(f'|2xx/5xx|{rate}|')
        print(f'|Success Rate|{total_2xx / total:.2f}|\n')


@dataclasses.dataclass
class Result:
    status: int
    highest_rate: float
    mean_rate: float
    total_number: int


def add_id(soup: bs4.BeautifulSoup) -> bs4.BeautifulSoup:
    """Errorsだけidが設定されていない。PR出してもいいかも。"""
    h3s = soup.find_all('h3')

    for h3 in h3s:
        if h3.text == "Errors":
            h3.attrs['id'] = "errors"

    return soup


def main(
        url: str,
        with_success_rate: bool) -> None:
    res = requests.get(url)
    txt = res.text.replace("</stats>", "</th>")  # 閉じタグを間違えている。PR提出済み
    soup = BeautifulSoup(txt, 'html.parser')
    soup = add_id(soup)

    for id_ in IDS[:]:
        header = soup.find(id=id_, class_="sub-header")
        if header is None:
            continue
        title = header.text.strip()
        table_response = header.next.next.next
        tables = table_response.find_all('table')

        print(f'## {title}')
        for table in tables:
            stats_table = StatsTable()
            trs = table.findChildren('tr', recursive=True)
            for i, tr in enumerate(trs):
                if i == 0:
                    stats_table.set_header(tr.find_all('th'))
                else:
                    stats_table.add_values(tr.find_all('td'))
            stats_table.print_table()

        if with_success_rate and id_ == 'http_status':
            stats_table.print_rate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', required=True, help="target url to make md table")
    parser.add_argument('--with-success-rate', '-w', action='store_true', help="print success rate")

    args = parser.parse_args()
    url = args.url
    with_success_rate = args.with_success_rate

    main(url, with_success_rate)
