""" Generate a markdown table for patterns listed on Azure Architecture Center.

Columns are,
1. Number
2. Title with hyperlink
3. Brian
4. Mike

Usage

```
pip install beautifulsoup4 requests
python generate_pattern_table.py
```
"""
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

PATTERN_INDEX_URL = "https://learn.microsoft.com/en-us/azure/architecture/patterns/"
TABLE_BODY_SELECTOR = "#main > div.content > table:nth-child(9) > tbody"


@dataclass
class Pattern:
    name: str
    _id: str

    @property
    def url(self):
        return PATTERN_INDEX_URL + self._id

    @classmethod
    def from_row(cls, row):
        return cls(name=row.a.string, _id=row.a["href"])


def print_md_table(patterns: list[Pattern]):
    header = "| # | pattern | Brian | Mike |"
    header_seperator = "| --- | --- | --- | --- |"
    output = "\n".join(
        (
            header,
            header_seperator,
            *(
                pattern_to_md_row(num, pattern)
                for num, pattern in enumerate(patterns, start=1)
            ),
        )
    )
    print(output)


def pattern_to_md_row(number: int, pattern: Pattern) -> str:
    return f"| {number} | [{pattern.name}]({pattern.url}) | | |"


def get_raw_page() -> str:
    response = requests.get(PATTERN_INDEX_URL)
    response.raise_for_status()
    return response.content


def parse_raw_page_to_patterns(raw: str) -> list[Pattern]:
    soup = BeautifulSoup(raw, "html.parser")
    table_body = soup.select_one(TABLE_BODY_SELECTOR)
    return [Pattern.from_row(row) for row in table_body.find_all("tr")]


if __name__ == "__main__":
    raw_page = get_raw_page()
    patterns = parse_raw_page_to_patterns(raw_page)
    print_md_table(patterns)
