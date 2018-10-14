import unittest
import requests
import requests_mock

from bears.general.URLHeadBear import URLHeadBear, LINK_CONTEXT, URLHeadResult
from coalib.results.SourceRange import SourceRange
from coalib.testing.LocalBearTestHelper import get_results
from coalib.settings.Section import Section
from queue import Queue
from .InvalidLinkBearTest import custom_matcher


class URLHeadBearTestPrerequisites(unittest.TestCase):

    def test_check_prerequisites(self):
        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)
            self.assertEqual(URLHeadBear.check_prerequisites(),
                             'You are not connected to the internet.')

            m.head(URLHeadBear.check_connection_url,
                   exc=requests.exceptions.RequestException)

            self.assertEqual(URLHeadBear.check_prerequisites(),
                             'You are not connected to the internet.')


class URLHeadBearTest(unittest.TestCase):
    """
    The tests are mocked (don't actually connect to internet) and
    return the int conversion of the last three chars of
    the URL as status code.

    Check ``custom matcher`` for more info on implementation.
    """

    def setUp(self):
        self.ib_check_prerequisites = URLHeadBear.check_prerequisites
        self.section = Section('')
        URLHeadBear.check_prerequisites = lambda *args: True
        self.uut = URLHeadBear(self.section, Queue())

    def tearDown(self):
        URLHeadBear.check_prerequisites = self.ib_check_prerequisites

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


class URLHeadResultTest(unittest.TestCase):

    def setUp(self):
        self.affected_code = (SourceRange.from_values('filename', 1),)

    def test_urlheadresult_wrong_type_link(self):
        msg = ('link must be an instance of one of '
               r'\(<class \'str\'>,\) \(provided value: 17072017\)')
        with self.assertRaisesRegex(TypeError, msg):
            URLHeadResult(URLHeadBear, self.affected_code, 17072017, Exception,
                          LINK_CONTEXT.no_context)

    def test_urlheadresult_wrong_type_http_status_code(self):
        msg = ('head_response must be an instance of one of '
               r'\(<class \'requests.models.Response\'>, '
               r'<class \'Exception\'>\) \(provided value: \'1\'\)')
        with self.assertRaisesRegex(TypeError, msg):
            URLHeadResult(URLHeadBear, self.affected_code, 'url', '1',
                          LINK_CONTEXT.no_context)

    def test_urlheadresult_wrong_type_link_context(self):
        msg = ('link_context must be an instance of one of '
               r'\(<aenum \'LINK_CONTEXT\'>,\)'
               r' \(provided value: \'LINK_CONTEXT\.no_context\'\)')
        with self.assertRaisesRegex(TypeError, msg):
            URLHeadResult(URLHeadBear, self.affected_code, 'url', Exception,
                          'LINK_CONTEXT.no_context')

    def test_urlheadresult_object_repr(self):
        resp_head = requests.models.Response()
        resp_head.status_code = 200
        repr_result = repr(URLHeadResult(URLHeadBear, self.affected_code,
                                         'http://google.com', resp_head,
                                         LINK_CONTEXT.no_context))
        repr_regex = (
            r'<URLHeadResult object\(id=.+, origin=\'bearclass\', '
            r'affected_code=\(<SourceRange object\(start=<SourcePosit'
            r'ion object\(file=\'.+\', line=1, column=None\) at .+>, '
            r'end=<SourcePosition object\(file=\'.+\', line=1, column'
            r'=None\) at .+>\) at .+>,\), message=\'http://google.com'
            r' responds with HTTP 200\', link=\'http://google.com\','
            r' http_status_code=200, link_context=<LINK_CONTEXT.no_co'
            r'ntext: 0>\, head_response=<Response \[200\]>\) at .+>')
        self.assertRegex(repr_result, repr_regex)
