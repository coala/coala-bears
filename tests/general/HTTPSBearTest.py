import io
from queue import Queue
import requests
import requests_mock
import unittest
import unittest.mock

from bears.general.HTTPSBear import HTTPSBear
from bears.general.URLHeadBear import URLHeadBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from tests.general.InvalidLinkBearTest import custom_matcher


def custom_matcher_https(request):
    """
    It is assumed that if the fourth last character is 'v' then the https
    version of the link returns the last three characters of the request
    URL to be the response and if it is 'i' then the https returns a 400
    code.

    For connection checking url, it always passes 200 (prerequisite checking).

    For URLs with no status codes appended, a ``RequestException`` is raised.

    To test for URLs that redirect to URLs with a much larger length, the
    ``redirect_long_url`` is returned.

    :param request: The ``request`` that the mocker recieves.
    :return:        A mocked ``Response`` object.
    """

    # the connection check url needs to be explicitly
    # set to 200
    if request.url == URLHeadBear.check_connection_url:
        status_code = 200
    else:
        try:
            if (request.path_url[-4] == 'v'):
                status_code = int(request.path_url[-3:])
            if (request.path_url[-4] == 'i'):
                status_code = 400
        except ValueError:
            raise requests.exceptions.RequestException
    resp = requests.Response()
    resp.raw = io.BytesIO()
    resp.status_code = status_code
    return resp


class HTTPSBearTestPrerequisites(unittest.TestCase):

    def test_check_prerequisites(self):
        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)
            self.assertTrue(URLHeadBear.check_prerequisites())

            m.head(URLHeadBear.check_connection_url,
                   exc=requests.exceptions.RequestException)

            self.assertTrue(URLHeadBear.check_prerequisites() ==
                            'You are not connected to the internet.')


class HTTPSBearTest(LocalBearTestHelper):
    """
    The tests are mocked (don't actually connect to the internet) and
    return the int conversion of the last three chars of
    the URL as status code.

    Check ``custom_matcher`` and ``custom_matcher_https`` for more info on
    implementation.
    """

    def setUp(self):
        self.ub_check_prerequisites = URLHeadBear.check_prerequisites
        self.section = Section('')
        URLHeadBear.check_prerequisites = lambda *args: True
        self.uut = HTTPSBear(self.section, Queue())

    def tearDown(self):
        URLHeadBear.check_prerequisites = self.ub_check_prerequisites

    def test_valid_https(self):
        test_link = """
        http://httpbin.org/status/v200
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher_https)
            self.check_line_result_count(self.uut, test_link, [1])

    def test_invalid_https(self):
        test_link = """
        http://httpbin.org/status/i200
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher_https)
            self.check_validity(self.uut, test_link)

    def test_https(self):
        test_link = """
        https://httpbin.org/status/v200
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher_https)
            self.check_validity(self.uut, test_link)
