import requests_mock
import unittest
import datetime

from queue import Queue

from bears.general.MementoFetchBear import MementoFetchBear
from bears.general.URLBear import URLBear
from coalib.results.SourceRange import SourceRange
from coalib.settings.Section import Section
from coalib.testing.LocalBearTestHelper import get_results

from .MementoBearTest import (custom_matcher, memento_archive_status_mock,
                              generate_redirects)


MEMENTOS = {'last': {
                'uri': ['http://web.archive.org/web/20170421070653/http://www'
                        '.google.com/'],
                'datetime': datetime.datetime(2017, 4, 21, 7, 6, 53)},
            'first': {'uri': ['http://web.archive.bibalex.org:80/web/1998'
                              '1111184551/http://google.com/'],
                      'datetime': datetime.datetime(1998, 11, 11, 18, 45, 51)},
            'closest': {'uri': ['http://web.archive.org/web/20170421070937/htt'
                                'ps://www.google.com/'],
                        'datetime': None, 'http_status_code': 200}}


class MementoFetchBearTest(unittest.TestCase):

    def setUp(self):
        self.ub_check_prerequisites = URLBear.check_prerequisites
        self.section = Section('')
        URLBear.check_prerequisites = lambda *args: True
        self.uut = MementoFetchBear(self.section, Queue())

    def tearDown(self):
        URLBear.check_prerequisites = self.ub_check_prerequisites

    def test_archived_links(self):
        valid_file = """
        https://www.google.com
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)
            # Register archived links
            memento_archive_status_mock(m, 'https://www.google.com')

            expected_affected_code = SourceRange.from_values('file', 2)
            results = get_results(self.uut, valid_file, filename='file')

            self.assertEqual(results[0].affected_code,
                             (expected_affected_code,))
            self.assertEqual(results[0].link, 'https://www.google.com')
            self.assertEqual(results[0].contents, MEMENTOS)
            self.assertEqual(results[0].redirected, False)

    def test_unarchived_links(self):
        valid_file = """
        http://unarchived.com
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)
            memento_archive_status_mock(m, 'http://unarchived.com', False)

            expected_affected_code = SourceRange.from_values('file', 2)
            results = get_results(self.uut, valid_file, filename='file')

            self.assertEqual(results[0].affected_code,
                             (expected_affected_code,))
            self.assertEqual(results[0].link, 'http://unarchived.com')
            self.assertEqual(results[0].contents, dict())
            self.assertEqual(results[0].redirected, False)

    def test_redirects(self):
        valid_file = """
        http://redirect2times.com
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)
            generate_redirects(m, 'http://redirect2times.com', 2)

            expected_affected_code = SourceRange.from_values('file', 2)
            results = get_results(self.uut, valid_file, filename='file')

            self.assertEqual(results[0].affected_code,
                             (expected_affected_code,))
            self.assertEqual(results[0].link, 'http://redirect2times.com')
            self.assertEqual(results[0].contents, dict())
            self.assertEqual(results[0].redirected, False)

            self.assertEqual(results[1].affected_code,
                             (expected_affected_code,))
            self.assertEqual(results[1].link, 'http://redirect2times.com/')
            self.assertEqual(results[1].contents, dict())
            self.assertEqual(results[1].redirected, True)

            self.assertEqual(results[2].affected_code,
                             (expected_affected_code,))
            self.assertEqual(results[2].link, 'http://redirect2times.com/1')
            self.assertEqual(results[2].contents, dict())
            self.assertEqual(results[2].redirected, True)
