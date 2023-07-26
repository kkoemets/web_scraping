import unittest

from tasks.email_tasks import IPhonePriceEmailSender


class IPhonePriceEmailSenderTest(unittest.TestCase):
    emailing_task = IPhonePriceEmailSender()

    def test_find_iphone_prices(self) -> None:
        self.emailing_task.send_iphone_prices()

    def test_find_ipad_prices(self) -> None:
        self.emailing_task.send_ipad_prices()


if __name__ == '__main__':
    unittest.main()
