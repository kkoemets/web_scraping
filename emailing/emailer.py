import os
import smtplib
from email.mime.text import MIMEText
from smtplib import SMTP

from dotenv import load_dotenv

load_dotenv()


class Emailer:
    @staticmethod
    def send_email(content: str) -> None:
        server: SMTP = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        sender_address: str = os.getenv('EMAILER_SENDER_ADDRESS', '')
        server.login(sender_address, os.getenv('EMAILER_SENDER_PASSWORD', ''))
        msg: str = MIMEText(content, 'html', _charset='utf-8').as_string()
        server.sendmail(sender_address, os.getenv('EMAILER_RECIPIENT_ADDRESS', ''), msg)
        server.quit()
