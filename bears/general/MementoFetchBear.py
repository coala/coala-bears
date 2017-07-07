import requests

from bears.general.URLBear import URLBear

from coala_utils.decorators import (enforce_signature, generate_ordering,
                                    generate_repr)
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.HiddenResult import HiddenResult
from coalib.results.SourceRange import SourceRange

from dependency_management.requirements.PipRequirement import PipRequirement

from memento_client import MementoClient


@generate_repr(('id', hex),
               'origin',
               'affected_code',
               'message',
               'link',
               'contents',
               'redirected')
@generate_ordering('affected_code',
                   'link',
                   'contents',
                   'redirected',
                   'origin',
                   'message_base')
class MementoFetchResult(HiddenResult):

    @enforce_signature
    def __init__(self, origin, affected_code,
                 link: str,
                 contents: dict,
                 redirected: bool):

        Result.__init__(self, origin,
                        'Archive info for (%s): %s' % (link, contents),
                        affected_code)
        self.link = link
        self.contents = contents
        self.redirected = redirected


class MementoFetchBear(LocalBear):
    DEFAULT_TIMEOUT = 15
    LANGUAGES = {'All'}
    REQUIREMENTS = {PipRequirement('memento_client', '0.6.1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Documentation'}
    BEAR_DEPS = {URLBear}

    @staticmethod
    def get_mementos(mc, link):
        """
        Get archive info of the link (mementos).

        :param mc:   A `memento_client.MementoClient` instance.
        :param link: The link (str) that will be checked.
        :return:     Dict, containing archive info of the link,
                     empty dict means the link is unarchived.
        """
        try:
            mementos = mc.get_memento_info(link)['mementos']
            return mementos
        except KeyError:
            return dict()

    @staticmethod
    def get_redirect_urls(link):
        urls = []

        resp = requests.head(link, allow_redirects=True)
        for redirect in resp.history:
            urls.append(redirect.url)

        return urls

    def run(self, filename, file, dependency_results=dict(),
            follow_redirects: bool = True):
        """
        Find links in any text file and give its archive information.

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

            affected_code = (SourceRange.from_values(filename, line_number),)

            if not (code and 200 <= code < 400):
                continue

            mementos = MementoFetchBear.get_mementos(self._mc, link)
            yield MementoFetchResult(self, affected_code, link, mementos,
                                     False)

            if follow_redirects and 300 <= code < 400:  # HTTP status 30x
                redirect_urls = MementoFetchBear.get_redirect_urls(link)
                for url in redirect_urls:
                    mementos = MementoFetchBear.get_mementos(self._mc, url)
                    yield MementoFetchResult(self, affected_code, url,
                                             mementos, True)
