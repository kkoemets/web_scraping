import logging
import os

from dotenv import load_dotenv

from emailing.emailer import Emailer
from ounaturg.ounaturg_parser import OunaturgParser, IPhoneModel
from utils.html_creator import HtmlCreator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

class IPhonePriceEmailSender:
    __emailer = Emailer()
    __parser = OunaturgParser()
    __html_creator = HtmlCreator()
    __price_threshold = int(os.getenv('EMAILING_IPHONE_PRICE_THRESHOLD', '999999'))

    def send_iphone_prices(self) -> None:
        prices = list(
            filter(lambda price: price.price <= self.__price_threshold,
                   self.__parser.find_iphone_prices(IPhoneModel.IPHONE_13_PRO_MAX)))

        if not prices:
            logging.info('No prices found, not sending an email')
            return

        self.__emailer.send_email(self.__html_creator.create_html_table([price._asdict() for price in prices]))
