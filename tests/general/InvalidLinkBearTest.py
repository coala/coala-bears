import requests
import unittest
from queue import Queue
import requests_mock

from bears.general.InvalidLinkBear import InvalidLinkBear
from coalib.settings.Section import Section


def custom_matcher(request):
    change_url = False
    try:
        status_code = int(request.path_url[-3:])
        if status_code in range(300, 400):
            change_url = True
            url = "some_url"
        resp = requests.Response()
        if change_url:
            resp.url = url
        resp.status_code = status_code
        return resp
    except ValueError:
        raise requests.exceptions.RequestException("")


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
        # Link Redirect
        valid_file = """
        http://httpbin.org/status/200
        """.splitlines()

        invalid_file = """
        http://httpbin.org/status/301
        http://coala.rtfd.org/302
        """.splitlines()

        self.assertResult(valid_file=valid_file, invalid_file=invalid_file)

        # Invalid Link Not Found
        valid_file = """
        http://httpbin.org/status/202
        """.splitlines()
        invalid_file = """
        http://httpbin.org/status/404
        http://httpbin.org/status/401
        """.splitlines()
        self.assertResult(valid_file=valid_file, invalid_file=invalid_file)

        # Invalid Link ServerError
        valid_file = """
        http://httpbin.org/status/202
        """.splitlines()
        invalid_file = """
        http://httpbin.org/status/500
        http://httpbin.org/status/503
        """.splitlines()
        self.assertResult(valid_file=valid_file, invalid_file=invalid_file)

        # Link Does Not Exist
        valid_file = """
           http://coala-analyzer.org/200\n
           http://coala-analyzer.org/200
           http://not a link dot com
           <http://lwn.net/200>
           'https://www.gnome.org/200'
           http://coala-analyzer.org/200.....
        """.splitlines()
        invalid_file = """
           http://coalaisthebest.com/
        """.splitlines()

        self.assertResult(valid_file=valid_file, invalid_file=invalid_file)

        # Mark down Links
        valid_file = """
            [coala](http://coala-analyzer.org/200)
            https://en.wikipedia.org/wiki/Hello_(Adele_song)/200
        """.splitlines()
        invalid_file = """
            http://coalaisthebest.com/
        """.splitlines()
        self.assertResult(valid_file=valid_file)

        # SphinxLinks
        valid_file = """
        |https://github.com/coala-analyzer/coala-bears/200|
        """.splitlines()
        self.assertResult(valid_file=valid_file)

    def test_check_prerequisites(self):
        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)
            self.assertIn("You are not", InvalidLinkBear.check_prerequisites())
            m.head("http://www.google.com")
            self.assertEqual(InvalidLinkBear.check_prerequisites(), True)
