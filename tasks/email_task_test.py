import unittest

from tasks.email_tasks import IPhonePriceEmailSender


class IPhonePriceEmailSenderTest(unittest.TestCase):
    emailing_task = IPhonePriceEmailSender()

    def test_find_iphone_prices(self) -> None:
        self.emailing_task.send_iphone_prices()


if __name__ == '__main__':
    unittest.main()
