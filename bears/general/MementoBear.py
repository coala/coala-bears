import requests

from bears.general.URLBear import URLBear

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY

from dependency_management.requirements.PipRequirement import PipRequirement

from memento_client import MementoClient


class MementoBear(LocalBear):
    DEFAULT_TIMEOUT = 15
    LANGUAGES = {'All'}
    REQUIREMENTS = {PipRequirement('memento_client', '0.6.1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Documentation'}
    BEAR_DEPS = {URLBear}

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

    def run(self, filename, file, dependency_results=dict(),
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

        :param dependency_results: Results given by URLBear.
        :param follow_redirects:   Set to true to check all redirect urls.
        """
        self._mc = MementoClient()

        for result in dependency_results.get(URLBear.name, []):
            line_number, link, code, context = result.contents

            if not (code and 200 <= code < 400):
                continue

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
