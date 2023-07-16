import unittest

from ounaturg_parser import find_iphone_prices


class TestOunaturg(unittest.TestCase):

    def test_find_iphone_prices(self):
        self.assertEqual('ok', find_iphone_prices('iphone', '64gb'))


if __name__ == '__main__':
    unittest.main()
