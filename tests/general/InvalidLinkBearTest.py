import requests
import unittest
from queue import Queue
import requests_mock

from bears.general.InvalidLinkBear import InvalidLinkBear
from coalib.settings.Section import Section


def custom_matcher(request):
    change_url = False
    # the connection check url needs to be explicitly
    # set to 200
    if request.url == InvalidLinkBear.check_connection_url:
        status_code = 200
    else:
        try:
            status_code = int(request.path_url[-3:])
        except ValueError:
            raise requests.exceptions.RequestException
    if status_code in range(300, 400):
        change_url = True
        url = "some_url"
    resp = requests.Response()
    if change_url:
        resp.url = url
    resp.status_code = status_code
    return resp


class InvalidLinkBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section("")

    def assertResult(self, valid_file=None, invalid_file=None):
        with requests_mock.Mocker() as m:
            InvalidLinkBear.check_prerequisites = lambda *args: True
            uut = InvalidLinkBear(self.section, Queue())
            m.add_matcher(custom_matcher)
            if valid_file:
                out = uut.execute("valid", valid_file)
                self.assertEqual(out, [])
            if invalid_file:
                out = uut.execute("invalid", invalid_file)
                self.assertNotEqual(out, [])
                self.assertNotEqual(out, None)

    def test_run(self):
        # Valid Links
        valid_file = """
        http://httpbin.org/status/200
        http://httpbin.org/status/201
        https://en.wikipedia.org/wiki/200
        """.splitlines()

        self.assertResult(valid_file=valid_file)

        # Link Redirect
        invalid_file = """
        http://httpbin.org/status/301
        http://httpbin.org/status/302
        """.splitlines()

        self.assertResult(invalid_file=invalid_file)

        # Invalid Link Not Found
        valid_file = """
        http://httpbin.org/status/401
        """
        invalid_file = """
        http://httpbin.org/status/404
        http://httpbin.org/status/410
        """.splitlines()

        self.assertResult(valid_file=valid_file, invalid_file=invalid_file)

        # Invalid Link ServerError
        invalid_file = """
        http://httpbin.org/status/500
        http://httpbin.org/status/503
        """.splitlines()

        self.assertResult(invalid_file=invalid_file)

        # Link Does Not Exist
        invalid_file = """
           http://coalaisthebest.com/
        """.splitlines()

        self.assertResult(invalid_file=invalid_file)

        # Test Regex
        valid_file = """
            https://en.wikipedia.org/wiki/Hello_(Adele_song)/200
            "https://github.com/coala-analyzer/coala-bears/issues/200"
            http://httpbin.org/status/200\n
            http://httpbin.org/status/201
            <http://httpbin.org/status/202>
            'http://httpbin.org/status/203'
            http://httpbin.org/status/204.....
            http://not a link dot com
        """.splitlines()

        self.assertResult(valid_file=valid_file)

        # Markdown Links
        valid_file = """
            [httpbin](http://httpbin.org/status/200)
        """.splitlines()

        self.assertResult(valid_file=valid_file)

        # Sphinx Links
        valid_file = """
        |http://httpbin.org/status/200|
        """.splitlines()

        self.assertResult(valid_file=valid_file)

    def test_check_prerequisites(self):
        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)
            self.assertTrue(InvalidLinkBear.check_prerequisites())
