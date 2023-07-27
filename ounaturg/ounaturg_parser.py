import logging
import re
from enum import Enum
from itertools import chain, takewhile, count
from typing import NamedTuple, Union

import requests
from bs4 import BeautifulSoup, Tag

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')


class IPhoneModel(Enum):
    IPHONE_13_PRO = 'iphone-13-pro'
    IPHONE_13_PRO_MAX = 'iphone-13-pro-max'


class IPadModel(Enum):
    IPAD_PRO = 'ipad-pro'


# abstract class
class ListingDetails(NamedTuple):
    price: float
    description: str
    model: str
    memory: str
    color: str
    condition: str
    location: str
    href: str


class IPhoneListingDetails(ListingDetails):
    pass


class IPadListingDetails(ListingDetails):
    pass


class OunaturgParser:
    __home_url: str = 'https://www.ounaturg.ee'
    __iphone_search_url: str = 'https://www.ounaturg.ee/iphone'
    __ipad_search_url: str = 'https://www.ounaturg.ee/ipad'
    _page_threshold: int = 50

    def find_iphone_prices(self, model: IPhoneModel) -> list[IPhoneListingDetails]:
        logging.info(f"Searching for {model.value} prices")

        details_urls = self._find_iphone_details_urls_bby_paginating(model)

        logging.info(f"Found {len(details_urls)} details urls")

        return [IPhoneListingDetails(*listing) for listing in
                (sorted([self._get_details_from_details_url(url) for url in details_urls], key=lambda a: a.price))]

    def find_ipad_prices(self, model: IPadModel) -> list[IPadListingDetails]:
        logging.info(f"Searching for {model.value} prices")

        details_urls = self._find_ipad_details_urls_by_paginating(model)

        logging.info(f"Found {len(details_urls)} details urls")

        return [IPadListingDetails(*listing) for listing in
                (sorted([self._get_details_from_details_url(url) for url in details_urls], key=lambda a: a.price))]

    def _find_iphone_details_urls_bby_paginating(self, model: IPhoneModel) -> list[str]:
        return self._find_details_urls_by_paginating(model, self.__iphone_search_url)

    def _find_ipad_details_urls_by_paginating(self, model: IPadModel) -> list[str]:
        return self._find_details_urls_by_paginating(model, self.__ipad_search_url)

    def _find_details_urls_by_paginating(self, model: Union[IPadModel, IPhoneModel], url: str) -> list[str]:
        return list(filter(lambda found_url: found_url.endswith(model.value),
                           list(chain.from_iterable(
                               takewhile(bool,
                                         (self._get_urls_to_offering_details(page, url) for page in
                                          count(start=1)))))))

    def _get_urls_to_offering_details(self, page_number: int, url: str) -> list[str]:
        if page_number > self._page_threshold:
            return []

        logging.info(f"Getting urls from page {page_number}")

        soup: BeautifulSoup = self._get_soup(f"{url}?page={page_number}")

        if soup.find(class_="pagination") is None and page_number > 1:
            return []

        urls = [] if soup.find(class_="next_page disabled") else \
            [self.__home_url + element.get("href") for element in (soup.find_all(attrs={"itemscope": "itemscope"}))]
        logging.info(f"Found {len(urls)} urls")
        return urls

    def _get_soup(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(self._get_html(url), "html.parser")

    def _get_details_from_details_url(self, url: str) -> ListingDetails:
        logging.info(f"Getting details from {url}")
        soup: BeautifulSoup = self._get_soup(url)

        listing_details = soup.find(class_="listing-details")

        found_details = [
            {"property_name": elements.find_all("span")[0].text, "property_value": elements.find_all("span")[1].text}
            for elements in (listing_details.find_all("li") if isinstance(listing_details, Tag) else [])]

        def _find_detail_value(detail_name: str) -> str:
            return next(
                (detail["property_value"] for detail in found_details if
                 detail["property_name"] == detail_name),
                "")

        def _to_number(numeric_string: str) -> float:
            return float(re.sub(r'[^0-9.]', '', numeric_string))

        description = soup.find(attrs={"itemprop": "description"})
        price = soup.find(attrs={"class": "listing-price"})
        return ListingDetails(
            price=_to_number(price.text) if price else -1.0,
            description=description.text if description else '',
            model=_find_detail_value("Mudel"),
            memory=_find_detail_value("Maht"),
            color=_find_detail_value("Värv"),
            condition=_find_detail_value("Seisukord"),
            location=_find_detail_value("Asukoht"),
            href=url)

    @staticmethod
    def _get_html(url: str) -> bytes:
        return requests.get(url).content
