import io
import json
import os
import requests
import requests_mock
import unittest

from bears.general.MementoBear import MementoBear
from bears.general.URLHeadBear import URLHeadBear
from bears.general.MementoFetchBear import MementoFetchBear

from coalib.results.Result import Result
from coalib.settings.Section import Section
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper

from queue import Queue


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'mementobear_test_files',
                        name)


# Load memento headers file
with open(get_testfile_path('google_memento_redirect_response.json')) as \
        headers1:
    with open(get_testfile_path('google_memento_timemap_response.json')) as \
            headers2:
        memento_headers = [json.load(headers1),
                           json.load(headers2)]


def custom_matcher(request):
    """
    Mock the status codes for every request by taking the last three characters
    of the request URL.

    For connection checking url, it always passes 200 (prerequisite checking).

    For URLs with no status codes appended, a ``RequestException`` is raised.

    :param request: The ``request`` that the mocker recieves.
    :return:        A mocked ``Response`` object.
    """

    # the connection check url needs to be explicitly
    # set to 200
    if request.url == URLHeadBear.check_connection_url:
        status_code = 200
    elif request.url.startswith('http://timetravel.mementoweb.org/timegate/'):
        # All memento timegate urls return 200
        status_code = 200
    else:
        try:
            status_code = int(request.path_url[-3:])
        except ValueError:
            raise requests.exceptions.RequestException('The selected string'
                                                       'cannot be converted to'
                                                       'integer')

    resp = requests.Response()
    resp.raw = io.BytesIO()
    resp.request = request
    resp.status_code = status_code
    return resp


def memento_archive_status_mock(m, url, is_archived=True, override_head=True):
    """
    Mock the memento result for the given url.

    :param m:             A `request_mock.Mocker()` instance.
    :param url:           The ``url`` to be mocked.
    :param is_archived:   True means the url will be marked as
                          archived.
    :param override_head: True means the url's head request will be overriden
                          by this method.
    """
    if override_head:
        m.head(url, headers={})
    if is_archived:
        # These two mocked responses will be received by memento_client
        # and make memento_client returns a fake archived link.
        # The first response headers will tell memento_client to redirect to
        # the second one.
        m.head(
            'http://timetravel.mementoweb.org/timegate/%s' % url,
            headers=memento_headers[0],
            status_code=302)
        m.head(
            'http://web.archive.org/web/20170421070937/'
            'https://www.google.com/',
            headers=memento_headers[1],
            status_code=200)
    else:
        m.head(
            'http://timetravel.mementoweb.org/timegate/%s' % url,
            status_code=404)


def generate_redirects(m, url, redirect_length=1):
    """
    Generate redirects path for the given url.

    :param m:               A `request_mock.Mocker()` instance.
    :param url:             The ``url`` to be redirected.
    :param redirect_length: How many redirects will be generated.
    """
    m.head(
        url,
        headers={'Location': '%s/1' % url},
        status_code=302)

    if redirect_length > 1:
        for i in range(redirect_length - 1):
            m.head(
                '%s/%s' % (url, str(i + 1)),
                headers={'Location': '%s/%s' % (url, str(i + 2))},
                status_code=302)

        m.head('%s/%s' % (url, str(redirect_length)),
               status_code=200)
    else:
        m.head('%s/1' % url, status_code=200)


class MementoBearTestPrerequisites(unittest.TestCase):

    def test_check_prerequisites(self):
        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)
            self.assertTrue(URLHeadBear.check_prerequisites())


class MementoBearTest(LocalBearTestHelper):
    """
    The tests are mocked (don't actually connect to internet) and
    return the int conversion of the last three chars of
    the URL as status code.

    Check ``custom matcher`` for more info on implementation.
    """

    def setUp(self):
        self.ub_check_prerequisites = URLHeadBear.check_prerequisites
        self.section = Section('')
        URLHeadBear.check_prerequisites = lambda *args: True
        self.uut = MementoBear(self.section, Queue())

    def tearDown(self):
        URLHeadBear.check_prerequisites = self.ub_check_prerequisites

    def test_dead_links(self):
        valid_file = """
        # Invalid/dead URLs should be ignored
        http://httpbin.org/status/404
        http://httpbin.org/status/410
        http://httpbin.org/status/500
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)
            self.check_validity(self.uut, valid_file)

    def test_archived_links(self):
        valid_file = """
        # Archived links should not yields error
        https://www.google.com
        https://www.facebook.com
        https://github.com/mementoweb/py-memento-client/
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)

            # Register archived links
            memento_archive_status_mock(m, 'https://www.google.com')
            memento_archive_status_mock(m, 'https://www.facebook.com')
            memento_archive_status_mock(
                m, 'https://github.com/mementoweb/py-memento-client/')

            self.check_validity(self.uut, valid_file)

    def test_unarchived_links(self):
        unarchived_links_file = """
        # Unarchived links should yields error
        https://www.facebook.com/coala
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)

            # Register not archived links
            memento_archive_status_mock(
                m, 'https://www.facebook.com/coala', False)

            self.check_results(
                self.uut,
                unarchived_links_file,
                [Result.from_values(
                    'MementoBear',
                    ('This link is not archived yet, visit '
                     'https://web.archive.org/save/https://www.facebook.com/co'
                     'ala to get it archived.'),
                    severity=RESULT_SEVERITY.INFO,
                    line=3,
                    file='default')],
                filename='default')

    def test_example_url(self):
        valid_file = """
        # Example.com URLs should be ignored
        http://sub.example.com/
        http://www.example.com/
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)
            self.check_validity(self.uut, valid_file)

    def test_multiple_results_per_line(self):
        test_file = """
        http://httpbin.org/status/410
        http://httpbin.org/status/200
        http://httpbin.org/status/404 http://httpbin.org/status/410
        http://httpbin.org/status/200 http://httpbin.org/status/404
        http://httpbin.org/status/200 http://httpbin.org/status/201
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)

            expected_num_results = [0, 1, 0, 1, 2]

            self.check_line_result_count(self.uut, test_file,
                                         expected_num_results)

    def test_redirect(self):
        invalid_file = """
        # Should yields error, even when the url has been archived,
        # but its redirects url are not archived yet.
        http://redirect9times.com
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)

            memento_archive_status_mock(m, 'http://redirect9times.com')
            generate_redirects(m, 'http://redirect9times.com', 9)

            redirect_links = MementoFetchBear.get_redirect_urls(
                'http://redirect9times.com')
            self.assertTrue(len(redirect_links) == 9)

            self.check_line_result_count(self.uut, invalid_file, [9])

            # Mark the first redirect url as archived
            memento_archive_status_mock(m, 'http://redirect9times.com/1',
                                        override_head=False)

            self.check_line_result_count(self.uut, invalid_file, [8])

    def test_settings_follow_redirects(self):
        invalid_file = """
        http://redirect5times.com
        """.splitlines()

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)
            generate_redirects(m, 'http://redirect5times.com', 5)

            # Mark the first url as archived
            memento_archive_status_mock(m, 'http://redirect5times.com',
                                        override_head=False)

            # Should yields error when `follow_redirects` is enabled
            self.check_invalidity(self.uut, invalid_file)

            # Should not yields any error, since the `follow_redirects` is
            # disabled
            self.check_validity(self.uut, invalid_file,
                                settings={'follow_redirects': False})

    def test_links_to_ignore(self):
        valid_file = """
        http://coalaisthebest.compile
        http://facebook.com/coala

        # Also for url that's not archived
        http://google.com
        """.splitlines()

        link_ignore_list = [
            'http://coalaisthebest.com',
            'http://mementoweb.org/[0-9][0-9]',
            'http://facebook.com/**',
            'http://google.com',
        ]

        with requests_mock.Mocker() as m:
            m.add_matcher(custom_matcher)

            memento_archive_status_mock(m, 'http://google.com', False)

            self.check_validity(
                self.uut, valid_file,
                settings={'link_ignore_list': link_ignore_list})
