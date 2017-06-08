import io
import logging
from queue import Queue
import requests
import requests_mock
import unittest
import unittest.mock

from bears.general.InvalidLinkBear import InvalidLinkBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section


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
    redirect_long_url = ('https://confluence.atlassian.com/bitbucket'
                         '/use-the-bitbucket-cloud-rest-apis-222724129.html')
    redirect_urls = ('https://bitbucket.org/api/301',
                     'https://bitbucket.org/api/302')

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
               'http://httpbin.org/get')
    resp = requests.Response()
    if change_url:
        resp.url = url
    resp.raw = io.BytesIO()
    resp.status_code = status_code
    return resp


class InvalidLinkBearTest(LocalBearTestHelper):
    """
    The tests are mocked (don't actually connect to internet) and
    return the int conversion of the last three chars of
    the URL as status code.

    Check ``custom matcher`` for more info on implementation.
    """

    def setUp(self):
        self.section = Section('')

    def assertResult(self, valid_file=None, invalid_file=None, settings={}):
        with requests_mock.Mocker() as m:
            InvalidLinkBear.check_prerequisites = lambda *args: True
            uut = InvalidLinkBear(self.section, Queue())
            m.add_matcher(custom_matcher)
            if valid_file:
                out = list(uut.run('valid', valid_file, **settings))
                self.assertEqual(out, [])
            if invalid_file:
                out = list(uut.run('invalid', invalid_file, **settings))
                self.assertNotEqual(out, [])
                self.assertNotEqual(out, None)

    def assertResultCount(self, test_file, expected_num):
        with requests_mock.Mocker() as m:
            InvalidLinkBear.check_prerequisites = lambda *args: True
            uut = InvalidLinkBear(self.section, Queue())
            m.add_matcher(custom_matcher)
            for line, num in zip(test_file, expected_num):
                outputs = list(uut.run('testline', [line]))
                self.assertEqual(num, len(outputs))

    def assertSeverity(self, file, severity, settings={}):
        """
        Test the warnings in each line of the file to match the
        given severity.
        :param file: The ``file`` to be checked.
        :param severity: The severity level of the warnings in each
                         line of the file.
        """
        severity_tag = RESULT_SEVERITY.reverse[severity]
        with requests_mock.Mocker() as m:
            uut = InvalidLinkBear(self.section, Queue())
            m.add_matcher(custom_matcher)
            outputs = list(uut.run('testfile', file, **settings))
            for out in outputs:
                out_dict = out.to_string_dict()
                self.assertEqual(severity_tag, out_dict['severity'])

    def test_run(self):
        # Valid Links
        valid_file = """
        http://httpbin.org/status/200
        http://httpbin.org/status/201
        http://httpbin.org/status/401  # Unauthorized

        # Parentheses
        https://en.wikipedia.org/wiki/Hello_(Adele_song)/200

        # Percentage after forward slash
        https://img.shields.io/badge/Maintained%3F-yes-green.svg

        # Quotes
        "https://github.com/coala/coala-bears/issues/200"
        'http://httpbin.org/status/203'
        ('http://httpbin.org/status/200').install_command()
        `https://coala.io/200`

        # Markup/down stuff
        <http://httpbin.org/status/202>
        http://httpbin.org/status/204.....
        [httpbin](http://httpbin.org/status/200)
        [http://httpbin.org/status/200](http://httpbin.org/status/200)
        |http://httpbin.org/status/200|
        <h3>Something http://httpbin.org/status/200</h3>
        repo=\\"http://httpbin.org/status/200\\"

        # Templated URLs can't be checked
        "http://httpbin.org/{status}/404".format(...)
        "http://httpbin.org/$status/404"

        # Not a link
        http://not a link dot com
        http://www.%s.com
        http://www.%d.com
        http://www.%f.com

        # Redirect
        http://httpbin.org/status/301
        http://httpbin.org/status/302

        # Example.com URLs should be ignored
        http://sub.example.com/404
        """.splitlines()

        self.assertResult(valid_file=valid_file)

        invalid_file = """
        http://coalaisthebest.com/
        http://httpbin.org/status/404
        http://httpbin.org/status/410
        http://httpbin.org/status/500
        http://httpbin.org/status/503
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)
            self.check_line_result_count(InvalidLinkBear(self.section,
                                                         Queue()),
                                         invalid_file, [1, 1, 1, 1, 1])

    def test_severity(self):
        normal_severity_file = """
        http://httpbin.org/status/404
        http://httpbin.org/status/410
        http://httpbin.org/status/500
        http://httpbin.org/status/503
        http://httpbin.org/status/301
        http://httpbin.org/status/302
        """.splitlines()

        self.assertSeverity(normal_severity_file, RESULT_SEVERITY.NORMAL)

        major_severity_file = """
        http://coalaisthebest.com
        """.splitlines()

        self.assertSeverity(major_severity_file, RESULT_SEVERITY.MAJOR)

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

    def test_multiple_results_per_line(self):

        test_file = """
        http://httpbin.org/status/410
        http://httpbin.org/status/200
        http://httpbin.org/status/404 http://httpbin.org/status/410
        http://httpbin.org/status/200 http://httpbin.org/status/404
        http://httpbin.org/status/200 http://httpbin.org/status/201
        """.splitlines()

        expected_num_results = [0, 1, 0, 2, 1, 0]

        self.assertResultCount(test_file, expected_num_results)

    def test_pip_vcs_url(self):
        with_at = """
        git+http://httpbin.org/status/200@master
        svn+http://httpbin.org/status/200@master
        hg+http://httpbin.org/status/200@master
        bzr+http://httpbin.org/status/200@master
        """.splitlines()

        self.assertResult(valid_file=with_at)

        with_hash = """
        git+http://httpbin.org/status/200#egg=coala-bears
        svn+http://httpbin.org/status/200#egg=coala-bears
        hg+http://httpbin.org/status/200#egg=coala-bears
        bzr+http://httpbin.org/status/200#egg=coala-bears
        """.splitlines()

        self.assertResult(valid_file=with_hash)

        with_at_hash = """
        git+http://httpbin.org/status/200@master#egg=coala-bears
        svn+http://httpbin.org/status/200@master#egg=coala-bears
        hg+http://httpbin.org/status/200@master#egg=coala-bears
        bzr+http://httpbin.org/status/200@master#egg=coala-bears
        """.splitlines()

        self.assertResult(valid_file=with_at_hash)

        brokenlink_at = """git+http://httpbin.org/status/404@master
        svn+http://httpbin.org/status/404@master
        hg+http://httpbin.org/status/404@master
        bzr+http://httpbin.org/status/404@master"""

        for line in brokenlink_at.splitlines():
            self.assertResult(invalid_file=[line])

        brokenlink_hash = """git+http://httpbin.org/status/404#egg=coala-bears
        svn+http://httpbin.org/status/404#egg=coala-bears
        hg+http://httpbin.org/status/404#egg=coala-bears
        bzr+http://httpbin.org/status/404#egg=coala-bears"""

        for line in brokenlink_hash.splitlines():
            self.assertResult(invalid_file=[line])

        brokenlink_at_hash = """git+http://httpbin.org/status/404@master#egg=coala-bears
        svn+http://httpbin.org/status/404@master#egg=coala-bears
        hg+http://httpbin.org/status/404@master#egg=coala-bears
        bzr+http://httpbin.org/status/404@master#egg=coala-bears"""

        for line in brokenlink_at_hash.splitlines():
            self.assertResult(invalid_file=[line])

    def test_xml_namespaces(self):
        valid_file = """
        #Namespace and also a valid link
        <ruleset name="test" xmlns="http://httpbin.org/status/200">

        # xml where xmlns: and xsi:schema are valid links
        <ruleset name="test" xmlns="http://xmlnamespace.org/status/200"
        xmlns:xsi="http://xmlnamespace.org/status/200"
        xsi:schemaLocation="http://xmlnamespace.org/status/200">
        """.splitlines()

        self.assertResult(valid_file=valid_file)

        invalid_file = """
        <ruleset name="test" xmlns="http://this.isa.namespace/ruleset/7.0.0"
        xmlns:xsi="http://this.is.another/kindof/namespace"
        xsi:schemaLocation="http://this.namespace.dosent/exists/7.0.0"
        xsi:schemaLocation="http://httpbin.com/404">""".splitlines()

        for line in invalid_file[1:]:
            self.assertResult(invalid_file=[line])

        info_severity_file = """
        <ruleset name="test" xmlns="http://this.is.a.namespace/ruleset/7.0.0"
        xmlns:xsi="http://this.is.another/kindof/namespace"
        xsi:schemaLocation="http://this.is.a.namespace/ruleset/7.0.0"/>

        <ruleset name="test" xmlns="http://a.new.namespace/ruleset/7.0.0"
        xmlns:xsi="http://another.namespace/ruleset/7.0.0"
        xsi:schemaLocation="http://another.namespace/ruleset/7.0.0"/>

        <layer-list xmlns:android="http://schema.android.com/apk/res/android"/>

        # Multiple ocurrences of namespaces
        <stylesheet xmlns="http://one.more.namespace/xsl/transform"
        xmlns:html="http://httpbin.com/200"
        xsi:schemaLocation="http://this.is.a.namespace/ruleset/7.0.0
                            http://another.namespace/ruleset/7.0.0
                            http://one.more.namespace/xsl/transform"/>
        """.splitlines()

        self.assertSeverity(info_severity_file, RESULT_SEVERITY.INFO)

        normal_severity_file = """
        xsi:schemaLocation="http://httpbin.com/404"
        """.splitlines()

        self.assertSeverity(normal_severity_file, RESULT_SEVERITY.NORMAL)

    def test_links_to_ignore(self):
        valid_file = """http://httpbin.org/status/200
        http://httpbin.org/status/201
        http://coalaisthebest.com/
        http://httpbin.org/status/404
        http://httpbin.org/status/410
        http://httpbin.org/status/500
        http://httpbin.org/status/503
        http://www.notexample.com/404
        http://exampe.com/404
        http://example.co.in/404""".splitlines()

        link_ignore_list = [
                           'http://coalaisthebest.com/',
                           'http://httpbin.org/status/4[0-9][0-9]',
                           'http://httpbin.org/status/410',
                           'http://httpbin.org/status/5[0-9][0-9]',
                           'http://httpbin.org/status/503',
                           'http://www.notexample.com/404',
                           'http://exampe.com/404',
                           'http://example.co.in/404'
                          ]

        self.assertResult(valid_file=valid_file,
                          settings={'link_ignore_list': link_ignore_list})

    def test_variable_timeouts(self):
        nt = {
            'https://google.com/timeout/test/2/3/4/5/something': 10,
            'https://facebook.com/timeout': 2,
            '*': 25
        }

        file_contents = """
        https://facebook.com/
        https://google.com/
        https://coala.io/som/thingg/page/123
        """.splitlines()

        def response(status_code, *args, **kwargs):
            res = requests.Response()
            res.status_code = status_code
            return res

        with unittest.mock.patch(
                'tests.general.InvalidLinkBearTest.requests.head',
                return_value=response(status_code=200)) as mock:
            uut = InvalidLinkBear(self.section, Queue())
            self.assertEqual([x.message
                              for x in list(uut.run('file', file_contents,
                                                    network_timeout=nt))], [])

            with self.assertLogs(logging.getLogger()) as log:
                self.assertEqual([x.message
                                  for x in list(uut.run('file', file_contents,
                                                        timeout=20))], [])
                self.assertEqual(log.output,
                                 ['WARNING:root:The setting `timeout` is '
                                  'deprecated. Please use `network_timeout` '
                                  'instead.'])

            self.assertEqual([x.message
                              for x in list(uut.run('file',
                                                    ['https://gitmate.io']))],
                             [])
            mock.assert_has_calls([
                unittest.mock.call('https://facebook.com/', timeout=2,
                                   allow_redirects=False),
                unittest.mock.call('https://google.com/',
                                   timeout=10, allow_redirects=False),
                unittest.mock.call('https://coala.io/som/thingg/page/123',
                                   timeout=25, allow_redirects=False),
                unittest.mock.call('https://facebook.com/', timeout=20,
                                   allow_redirects=False),
                unittest.mock.call('https://google.com/',
                                   timeout=20, allow_redirects=False),
                unittest.mock.call('https://coala.io/som/thingg/page/123',
                                   timeout=20, allow_redirects=False),
                unittest.mock.call('https://gitmate.io',
                                   timeout=15, allow_redirects=False)])
