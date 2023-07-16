import unittest

from emailing.emailer import Emailer


class EmailerTest(unittest.TestCase):
    emailer = Emailer()

    def test_send_email(self):
        self.emailer.send_email('<p>hi£</p>')


if __name__ == '__main__':
    unittest.main()
