import logging

from emailing.emailer import Emailer
from ounaturg.ounaturg_parser import OunaturgParser, IPhoneModel
from utils.html_creator import HtmlCreator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')


class IPhonePriceEmailSender:
    __emailer = Emailer()
    __parser = OunaturgParser()
    __html_creator = HtmlCreator()

    def send_iphone_prices(self) -> None:
        prices = self.__parser.find_iphone_prices(IPhoneModel.IPHONE_13_PRO_MAX)
        if not prices:
            logging.info('No prices found, not sending an email')
            return
        self.__emailer.send_email(self.__html_creator.create_html_table([price._asdict() for price in prices]))
