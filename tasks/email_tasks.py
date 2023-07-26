import logging
import os

from dotenv import load_dotenv

from emailing.emailer import Emailer
from ounaturg.ounaturg_parser import OunaturgParser, IPhoneModel, IPadModel
from utils.html_creator import HtmlCreator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()


class IPhonePriceEmailSender:
    __emailer = Emailer()
    __parser: OunaturgParser = OunaturgParser()
    __html_creator: HtmlCreator = HtmlCreator()
    __price_threshold = int(os.getenv('EMAILING_IPHONE_PRICE_THRESHOLD', '999999'))
    __ignored_listings: list[str] = os.getenv('EMAILING_IPHONE_IGNORED_LISTINGS', ' ').split(',')

    def send_iphone_prices(self) -> None:
        listings = list(
            filter(lambda listing: all(not listing.href.endswith(ignored) for ignored in self.__ignored_listings),
                   list(filter(lambda listing: listing.price <= self.__price_threshold,
                               self.__parser.find_iphone_prices(IPhoneModel.IPHONE_13_PRO_MAX)))))

        if not listings:
            logging.info('No matching iphone listings found, not sending an email')
            return

        self.__emailer.send_email(self.__html_creator.create_html_table([price._asdict() for price in listings]))

    def send_ipad_prices(self) -> None:
        listings = self.__parser.find_ipad_prices(IPadModel.IPAD_PRO)

        if not listings:
            logging.info('No matching ipad listings found, not sending an email')
            return

        self.__emailer.send_email(self.__html_creator.create_html_table([price._asdict() for price in listings]))
