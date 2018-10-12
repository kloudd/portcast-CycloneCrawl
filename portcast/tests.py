"""
    This is the testcase file.
    It We have created the fake http response and dumped page source,
    in the data/**.html files.
    To run - python3 tests.py
    - Sumit Singh Kanwal
"""
import os
from unittest.case import TestCase
from scrapy.http import Request, TextResponse
from .spiders.cyclone import CycloneSpider


def fake_response(file_name=None, url=None):
    """Create a Scrapy fake HTTP response from a HTML file"""
    if not url:
        url = 'http://rammb.cira.colostate.edu/products/tc_realtime/index.asp'

    request = Request(url=url)
    if file_name:
        if not file_name[0] == '/':
            responses_dir = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(responses_dir, file_name)
        else:
            file_path = file_name

        file_content = open(file_path, 'r').read()
    else:
        file_content = ''

    response = TextResponse(url=url, request=request, body=file_content,
                            encoding='utf-8')
    return response


class MyTestCase(TestCase):
    """
    This is the test case class which will check the http requested data,
    to the dumped data.
    """

    def setUp(self):
        """
        Initial configs and data for the test class.
        """
        self.files = ['data/AL132018.html', 'data/AL142018.html', 'data/AL152018.html',
                      'data/EP212018.html', 'data/IO052018.html', 'data/IO062018.html']

        self.spider = CycloneSpider()

    def test_parse(self):
        """
        Function to test responses.
        """
        response = fake_response(self.files[0])
        items = self.spider.parse_item(response)
        for item in items:
            self.assertEqual(item['name'][0], 'AL132018 - Hurricane LESLIE')

        response = fake_response(self.files[1])
        items = self.spider.parse_item(response)
        for item in items:
            self.assertEqual(item['name'][0], 'AL142018 - Tropical Storm MICHAEL')

        response = fake_response(self.files[2])
        items = self.spider.parse_item(response)
        for item in items:
            self.assertEqual(item['name'][0], 'AL152018 - Tropical Storm NADINE')

        response = fake_response(self.files[3])
        items = self.spider.parse_item(response)
        for item in items:
            self.assertEqual(item['name'][0], 'EP212018 - Tropical Storm SERGIO')

        response = fake_response(self.files[4])
        items = self.spider.parse_item(response)
        for item in items:
            self.assertEqual(item['name'][0], 'IO052018 - Tropical Cyclone (<64 kt) LUBAN')

        response = fake_response(self.files[5])
        items = self.spider.parse_item(response)
        for item in items:
            self.assertEqual(item['name'][0], 'IO062018 - Tropical Cyclone (<64 kt) TITLI')
