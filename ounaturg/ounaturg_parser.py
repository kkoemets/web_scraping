import logging
import re
from enum import Enum
from itertools import chain, takewhile, count
from typing import NamedTuple

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class IPhoneModel(Enum):
    IPHONE_13_PRO = 'iphone-13-pro'
    IPHONE_13_PRO_MAX = 'iphone-13-pro-max'


class IPhoneListingDetails(NamedTuple):
    price: str
    description: str
    model: str
    memory: str
    color: str
    condition: str
    location: str
    href: str


class OunaturgParser:
    HOME_URL = 'https://www.ounaturg.ee'
    IPHONE_SEARCH_URL = 'https://www.ounaturg.ee/iphone'

    def find_iphone_prices(self, model: IPhoneModel) -> list[IPhoneListingDetails]:
        logging.info(f"Searching for {model.value} prices")

        def _get_details(page):
            return self._get_urls_to_offering_details(page)

        def _filter_by_model(url: str) -> bool:
            return url.endswith(model.value)

        details_urls = list(filter(_filter_by_model,
                                   list(chain.from_iterable(
                                       takewhile(bool, (_get_details(page) for page in count(start=1)))))))

        logging.info(f"Found {len(details_urls)} details urls")

        def _to_number(numeric_string: str) -> float:
            return float(re.sub(r'[^0-9.]', '', numeric_string))

        return sorted([self._get_details_from_details_url(url) for url in details_urls],
                      key=lambda a: _to_number(a.price))

    def _get_urls_to_offering_details(self, page_number: int) -> list[str]:
        logging.info(f"Getting urls from page {page_number}")

        soup = self._get_soup(f"{self.IPHONE_SEARCH_URL}?page={page_number}")

        urls = [] if soup.find(class_="next_page disabled") else \
            [self.HOME_URL + element.get("href") for element in (soup.find_all(attrs={"itemscope": "itemscope"}))]
        logging.info(f"Found {len(urls)} urls")
        return urls

    def _get_soup(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(self._get_html(url), "html.parser")

    @staticmethod
    def _get_html(url: str) -> bytes:
        return requests.get(url).content

    def _get_details_from_details_url(self, url: str) -> IPhoneListingDetails:
        logging.info(f"Getting details from {url}")
        soup = self._get_soup(url)

        find = soup.find(class_="listing-details").find_all("li")

        details_collector = []
        for elements in find:
            elements = elements.find_all("span")
            details_collector.append({"proparty_name": elements[0].text, "proparty_value": elements[1].text})

        def _find_detail_value(detail_name: str) -> str:
            return next(
                (detail["proparty_value"] for detail in details_collector if
                 detail["proparty_name"] == detail_name),
                "")

        description = soup.find(attrs={"itemprop": "description"})
        return IPhoneListingDetails(
            price=soup.find(attrs={"class": "listing-price"}).text,
            description=description.text if description else '',
            model=_find_detail_value("Mudel"),
            memory=_find_detail_value("Maht"),
            color=_find_detail_value("Värv"),
            condition=_find_detail_value("Seisukord"),
            location=_find_detail_value("Asukoht"),
            href=url
        )
