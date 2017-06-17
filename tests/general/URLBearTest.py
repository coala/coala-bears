import unittest
import requests
import requests_mock

from bears.general.URLBear import URLBear, LINK_CONTEXT
from coalib.testing.LocalBearTestHelper import get_results
from coalib.settings.Section import Section
from queue import Queue
from .InvalidLinkBearTest import custom_matcher


class URLBearTestPrerequisites(unittest.TestCase):

    def test_check_prerequisites(self):
        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)
            self.assertTrue(URLBear.check_prerequisites())

            m.head(URLBear.check_connection_url,
                   exc=requests.exceptions.RequestException)

            self.assertTrue(URLBear.check_prerequisites() ==
                            'You are not connected to the internet.')


class URLBearTest(unittest.TestCase):
    """
    The tests are mocked (don't actually connect to internet) and
    return the int conversion of the last three chars of
    the URL as status code.

    Check ``custom matcher`` for more info on implementation.
    """

    def setUp(self):
        self.ib_check_prerequisites = URLBear.check_prerequisites
        self.section = Section('')
        URLBear.check_prerequisites = lambda *args: True
        self.uut = URLBear(self.section, Queue())

    def tearDown(self):
        URLBear.check_prerequisites = self.ib_check_prerequisites

    def test_detect_url_result(self):
        valid_file = """
        http://www.facebook.com/200
        http://www.google.com/404
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)

            result = get_results(self.uut, valid_file)
            self.assertEqual(result[0].contents,
                             [2, 'http://www.facebook.com/200',
                              200, LINK_CONTEXT.no_context])
            self.assertEqual(result[1].contents,
                             [3, 'http://www.google.com/404',
                              404, LINK_CONTEXT.no_context])
