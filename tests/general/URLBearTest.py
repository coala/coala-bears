import unittest
import requests
import requests_mock

from bears.general.URLBear import URLBear, LINK_CONTEXT, URLResult
from coalib.results.SourceRange import SourceRange
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


class URLResultTest(unittest.TestCase):

    def setUp(self):
        self.affected_code = (SourceRange.from_values('filename', 1),)

    def test_urlresult_wrong_type_link(self):
        msg = ('link must be an instance of one of '
               '\(<class \'str\'>,\) \(provided value: 17072017\)')
        with self.assertRaisesRegex(TypeError, msg):
            URLResult(URLBear, self.affected_code, 17072017, 1,
                      LINK_CONTEXT.no_context)

    def test_urlresult_wrong_type_http_status_code(self):
        msg = ('http_status_code must be an instance of one of '
               '\(<class \'int\'>, None\) \(provided value: \'1\'\)')
        with self.assertRaisesRegex(TypeError, msg):
            URLResult(URLBear, self.affected_code, 'url', '1',
                      LINK_CONTEXT.no_context)

    def test_urlresult_wrong_type_link_context(self):
        msg = ('link_context must be an instance of one of '
               '\(<aenum \'LINK_CONTEXT\'>,\)'
               ' \(provided value: \'LINK_CONTEXT\.no_context\'\)')
        with self.assertRaisesRegex(TypeError, msg):
            URLResult(URLBear, self.affected_code, 'url', 1,
                      'LINK_CONTEXT.no_context')

    def test_urlresult_object_repr(self):
        repr_result = repr(URLResult(URLBear, self.affected_code,
                                     'http://google.com', 200,
                                     LINK_CONTEXT.no_context))
        repr_regex = ('<URLResult object\(id=.+, origin=\'bearclass\', '
                      'affected_code=\(<SourceRange object\(start=<SourcePosit'
                      'ion object\(file=\'.+\', line=1, column=None\) at .+>, '
                      'end=<SourcePosition object\(file=\'.+\', line=1, column'
                      '=None\) at .+>\) at .+>,\), message=\'http://google.com'
                      ' responds with HTTP 200\', link=\'http://google.com\','
                      ' http_status_code=200, link_context=<LINK_CONTEXT.no_co'
                      'ntext: 0>\) at .+>')
        self.assertRegex(repr_result, repr_regex)
