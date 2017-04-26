import requests

from bears.general.InvalidLinkBear import InvalidLinkBear

from coalib.settings.Setting import typed_dict
from coalib.settings.Setting import typed_list
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY

from dependency_management.requirements.PipRequirement import PipRequirement

from memento_client import MementoClient

from urllib.parse import urlparse


class MementoBear(InvalidLinkBear):
    DEFAULT_TIMEOUT = 15
    LANGUAGES = {'All'}
    REQUIREMENTS = {PipRequirement('memento_client', '0.5.3')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Documentation'}
    DEFAULT_IGNORE = [
        'http://web.archive.org/**',
    ]

    def analyze_links_in_file(self, file, network_timeout, link_ignore_regex,
                              link_ignore_list):
        for link, line_number, link_context in self.extract_links_from_file(
                file, link_ignore_regex, link_ignore_list):

            host = urlparse(link).netloc
            code = InvalidLinkBear.get_status_code(
                link,
                network_timeout.get(host)
                if host in network_timeout
                else network_timeout.get('*')
                if '*' in network_timeout
                else self.DEFAULT_TIMEOUT)
            if code and 200 <= code < 400:
                yield line_number + 1, link, code, link_context

    @staticmethod
    def check_archive(mc, link):
        """
        Check the link is it archived or not.

        :param mc:   A `memento_client.MementoClient` instance.
        :param link: The link (str) that will be checked.
        :return:     Boolean, `True` means the link has been archived.
        """
        try:
            mc.get_memento_info(link)['mementos']
        except KeyError:
            return False
        return True

    @staticmethod
    def get_redirect_urls(link):
        urls = []

        resp = requests.head(link, allow_redirects=True)
        for redirect in resp.history:
            urls.append(redirect.url)

        return urls

    def run(self, filename, file,
            network_timeout: typed_dict(str, int, DEFAULT_TIMEOUT)=dict(),
            link_ignore_regex: str='([.\/]example\.com|\{|\$)',
            link_ignore_list: typed_list(str)=DEFAULT_IGNORE,
            follow_redirects: bool=True):
        """
        Find links in any text file and check if they are archived.

        Link is considered valid if the link has been archived by any services
        in memento_client.

        This bear can automatically fix redirects.

        Warning: This bear will make HEAD requests to all URLs mentioned in
        your codebase, which can potentially be destructive. As an example,
        this bear would naively just visit the URL from a line that goes like
        `do_not_ever_open = 'https://api.acme.inc/delete-all-data'` wiping out
        all your data.

        :param network_timeout:    A dict mapping URLs and timeout to be
                                   used for that URL. All the URLs that have
                                   the same host as that of URLs provided
                                   will be passed that timeout. It can also
                                   contain a wildcard timeout entry with key
                                   '*'. The timeout of all the websites not
                                   in the dict will be the value of the key
                                   '*'.
        :param link_ignore_regex:  A regex for urls to ignore.
        :param link_ignore_list:   Comma separated url globs to ignore.
        :param follow_redirects:   Set to true to check all redirect urls.
        """
        self._mc = MementoClient()

        network_timeout = {urlparse(url).netloc
                           if not url == '*' else '*': timeout
                           for url, timeout in network_timeout.items()}

        if link_ignore_list != self.DEFAULT_IGNORE:
            link_ignore_list.extend(self.DEFAULT_IGNORE)

        for (line_number, link,
             code, context) in self.analyze_links_in_file(
                file, network_timeout, link_ignore_regex, link_ignore_list):
            status = MementoBear.check_archive(self._mc, link)
            if not status:
                yield Result.from_values(
                    self,
                    ('This link is not archived yet, visit '
                     'https://web.archive.org/save/%s to get it archived.'
                     % link),
                    file=filename,
                    line=line_number,
                    severity=RESULT_SEVERITY.INFO
                )

            if follow_redirects and 300 <= code < 400:  # HTTP status 30x
                redirect_urls = MementoBear.get_redirect_urls(link)

                for url in redirect_urls:
                    status = MementoBear.check_archive(self._mc, url)
                    if not status:
                        yield Result.from_values(
                            self,
                            ('This link redirects to %s and not archived yet, '
                             'visit https://web.archive.org/save/%s to get it '
                             'archived.'
                             % (url, url)),
                            file=filename,
                            line=line_number,
                            severity=RESULT_SEVERITY.INFO
                        )
