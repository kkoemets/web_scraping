import unittest

from utils.html_creator import HtmlCreator


class HtmlCreatorTest(unittest.TestCase):
    creator = HtmlCreator()

    def test_create_html(self) -> None:
        self.assertEqual(self.creator.create_html_table([
            dict(
                price=1000.0,
                description='description',
                model='model',
                memory='memory',
                color='color',
                condition='condition',
                location='location',
                href='href'),
            dict(
                price=1100.0,
                description='description',
                model='model',
                memory='memory',
                color='color',
                condition='condition',
                location='location',
                href='href')]),
            """
        
        <style type="text/css">
        table {
            border-collapse: collapse;
            width: 100%;
            text-align: left;
        }
        th, td {
            padding: 8px;
            border-bottom: 1px solid green;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        </style>
        
        <table>
          <thead>
            <tr>
              <th>Price</th><th>Description</th><th>Model</th><th>Memory</th><th>Color</th><th>Condition</th><th>Location</th><th>Href</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>1000.0</td><td>description</td><td>model</td><td>memory</td><td>color</td><td>condition</td><td>location</td><td>href</td></tr><tr><td>1100.0</td><td>description</td><td>model</td><td>memory</td><td>color</td><td>condition</td><td>location</td><td>href</td></tr>
          </tbody>
        </table>""")
