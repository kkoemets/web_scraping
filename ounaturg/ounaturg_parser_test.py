import unittest

from ounaturg.ounaturg_parser import IPhoneModel, OunaturgParser, IPadModel


class OunaturgParserTest(unittest.TestCase):
    parser = OunaturgParser()
    parser._page_threshold = 2

    def test_find_ipad_prices(self) -> None:
        self.assertTrue(self.parser.find_ipad_prices(IPadModel.IPAD_PRO))

    def test_find_iphone_prices(self) -> None:
        self.assertTrue(self.parser.find_iphone_prices(IPhoneModel.IPHONE_13_PRO))

    def test_get_links_to_offering_details(self) -> None:
        found_links = self.parser._get_urls_to_offering_details(1, 'https://www.ounaturg.ee/iphone')
        self.assertTrue(found_links)
        for link in found_links:
            self.assertIn('https://www.ounaturg.ee', link)

    def test_get_details_from_details_url(self) -> None:
        listing = self.parser._get_details_from_details_url('https://www.ounaturg.ee/46985-iphone-13-pro')
        self.assertTrue(listing.price)
        self.assertTrue(listing.description)
        self.assertTrue(listing.model)
        self.assertTrue(listing.memory)
        self.assertTrue(listing.color)
        self.assertTrue(listing.condition)
        self.assertTrue(listing.location)
        self.assertTrue(listing.href)
        self.assertTrue(listing.listing_age)


if __name__ == '__main__':
    unittest.main()
