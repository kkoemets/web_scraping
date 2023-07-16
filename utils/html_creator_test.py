import unittest

from html_creator import HtmlCreator


class HtmlCreatorTest(unittest.TestCase):
    creator = HtmlCreator()

    def test_create_html(self):
        self.assertEqual(self.creator.create_html_table([
            dict(
                price='1000$',
                description='description',
                model='model',
                memory='memory',
                color='color',
                condition='condition',
                location='location',
                href='href'
            ),
            dict(
                price='1100$',
                description='description',
                model='model',
                memory='memory',
                color='color',
                condition='condition',
                location='location',
                href='href'
            )
        ]),
            '<table><tr><td>1000$</td><td>description</td><td>model</td><td>memory</td><td>color</td><td>condition'
            '</td><td>location</td><td>href</td></tr><tr><td>1100$</td><td>description</td><td>model</td><td>memory'
            '</td><td>color</td><td>condition</td><td>location</td><td>href</td></tr></table>')
