from flask import Flask
from flask_apscheduler import APScheduler
from pytz import timezone

from tasks.email_tasks import IPhonePriceEmailSender

mailer = IPhonePriceEmailSender()


class Config:
    SCHEDULER_API_ENABLED = True


def setup_cron(app: Flask) -> None:
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='send_iphone_prices', func=mailer.send_iphone_prices, trigger='cron', hour=8,
                      timezone=timezone('Europe/Helsinki'))
