import logging
from enum import Enum
from typing import NamedTuple

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class IPhoneModel(Enum):
    IPHONE_13_PRO = 'iPhone%2013%20Pro'


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

        details_urls = list(
            {url for page_number in range(1, 3) for url in self._get_urls_to_offering_details(model, page_number)})
        logging.info(f"Found {len(details_urls)} details urls")

        return [self._get_details_from_details_url(url) for url in details_urls]

    def _get_urls_to_offering_details(self, model: IPhoneModel, page_number: int) -> list[str]:
        return [self.HOME_URL + element.get("href") for element in (
            self._get_soup(f"{self.IPHONE_SEARCH_URL}/mudel-{model.value}?page={page_number}")
            .find_all(attrs={"itemscope": "itemscope"}))]

    @staticmethod
    def _get_html(url: str) -> bytes:
        return requests.get(url).content

    def _get_soup(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(self._get_html(url), "html.parser")

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
