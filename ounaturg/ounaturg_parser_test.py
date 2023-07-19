import unittest

from ounaturg_parser import IPhoneModel, OunaturgParser


class OunaturgParserTest(unittest.TestCase):
    parser = OunaturgParser()

    def test_find_iphone_prices(self):
        self.assertTrue(self.parser.find_iphone_prices(IPhoneModel.IPHONE_13_PRO))

    def test_get_links_to_offering_details(self):
        found_links = self.parser._get_urls_to_offering_details(1)
        self.assertTrue(found_links)
        for link in found_links:
            self.assertIn('https://www.ounaturg.ee', link)

    def test_get_details_from_details_url(self):
        listing = self.parser._get_details_from_details_url('https://www.ounaturg.ee/46985-iphone-13-pro')
        self.assertTrue(listing.price)
        self.assertTrue(listing.description)
        self.assertTrue(listing.model)
        self.assertTrue(listing.memory)
        self.assertTrue(listing.color)
        self.assertTrue(listing.condition)
        self.assertTrue(listing.location)
        self.assertTrue(listing.href)


if __name__ == '__main__':
    unittest.main()
