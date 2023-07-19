from flask_apscheduler import APScheduler
from pytz import timezone

from emailing.emailer import Emailer
from ounaturg.ounaturg_parser import OunaturgParser, IPhoneModel
from utils.html_creator import HtmlCreator


class Config:
    SCHEDULER_API_ENABLED = True


def setup_cron(app):
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='send_iphone_prices', func=send_iphone_prices, trigger='cron', hour=8,
                      timezone=timezone('Europe/Helsinki'))


def send_iphone_prices():
    emailer = Emailer()
    parser = OunaturgParser()
    html_creator = HtmlCreator()
    prices = parser.find_iphone_prices(IPhoneModel.IPHONE_13_PRO_MAX)
    emailer.send_email(html_creator.create_html_table([price._asdict() for price in prices]))
