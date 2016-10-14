import requests
import unittest
from queue import Queue
import requests_mock

from bears.general.InvalidLinkBear import InvalidLinkBear
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


def custom_matcher(request):
    """
    Mock the status codes for every request by taking the last three characters
    of the request URL.

    For connection checking url, it always passes 200 (prerequisite checking).

    For URLs with no status codes appended, a ``RequestException`` is raised.

    To test for URLs that redirect to URLs with a much larger length, the
    ``redirect_long_url`` is returned.

    :param request: The ``request`` that the mocker recieves.
    :return:        A mocked ``Response`` object.
    """
    redirect_long_url = ("https://confluence.atlassian.com/bitbucket"
                         "/use-the-bitbucket-cloud-rest-apis-222724129.html")
    redirect_urls = ("https://bitbucket.org/api/301",
                     "https://bitbucket.org/api/302")

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
        url = (redirect_long_url if request.url in redirect_urls else
               "http://httpbin.org/get")
    resp = requests.Response()
    if change_url:
        resp.url = url
    resp.status_code = status_code
    return resp


class InvalidLinkBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section("")

    def assertResult(self, valid_file=None, invalid_file=None, settings={}):
        with requests_mock.Mocker() as m:
            InvalidLinkBear.check_prerequisites = lambda *args: True
            uut = InvalidLinkBear(self.section, Queue())
            for name, value in settings.items():
                self.section.append(Setting(name, value))
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
        http://httpbin.org/status/401  # Unauthorized

        # Parentheses
        https://en.wikipedia.org/wiki/Hello_(Adele_song)/200

        # Quotes
        "https://github.com/coala/coala-bears/issues/200"
        'http://httpbin.org/status/203'
        ('http://httpbin.org/status/200').install_command()
        `https://coala.io/200`

        # Markup/down stuff
        <http://httpbin.org/status/202>
        http://httpbin.org/status/204.....
        [httpbin](http://httpbin.org/status/200)
        |http://httpbin.org/status/200|
        <h3>Something http://httpbin.org/status/200</h3>
        repo=\\"http://httpbin.org/status/200\\"

        # Templated URLs can't be checked
        "http://httpbin.org/{status}/404".format(...)
        "http://httpbin.org/$status/404"

        # Not a link
        http://not a link dot com

        # Redirect
        http://httpbin.org/status/301
        http://httpbin.org/status/302
        """.splitlines()

        self.assertResult(valid_file=valid_file)

        invalid_file = """http://coalaisthebest.com/
        http://httpbin.org/status/404
        http://httpbin.org/status/410
        http://httpbin.org/status/500
        http://httpbin.org/status/503"""

        for line in invalid_file.splitlines():
            self.assertResult(invalid_file=[line])

    def test_check_prerequisites(self):
        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)
            self.assertTrue(InvalidLinkBear.check_prerequisites())

    def test_redirect_threshold(self):

        long_url_redirect = """
        https://bitbucket.org/api/301
        https://bitbucket.org/api/302
        """.splitlines()

        short_url_redirect = """
        http://httpbin.org/status/301
        """.splitlines()

        self.assertResult(valid_file=long_url_redirect,
                          invalid_file=short_url_redirect,
                          settings={'follow_redirects': 'yeah'})

    def test_link_ignore_regex(self):

        ignored_URLs = """
        http://sub.example.com
        http://sub.example.com/something
        """.splitlines()

        not_ignored_URLs = """
        http://www.notexample.com
        http://exampe.com
        http://example.co.in
        """.splitlines()

        self.assertResult(valid_file=ignored_URLs,
                          invalid_file=not_ignored_URLs)

        valid_file = """
        http://httpbin.org/status/524
        """.splitlines()
        invalid_file = """
        http://httpbin.org/status/503
        """.splitlines()
        self.assertResult(valid_file=valid_file,
                          invalid_file=invalid_file,
                          settings={'link_ignore_regex': '[1-9]{2}$'})
