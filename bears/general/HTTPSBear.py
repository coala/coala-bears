from urllib.parse import urlparse

from bears.general.URLHeadBear import URLHeadBear
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY

from coalib.results.Diff import Diff
from coalib.settings.Setting import typed_dict


class HTTPSBear(LocalBear):
    DEFAULT_TIMEOUT = 15
    LANGUAGES = {'All'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Documentation'}
    CAN_FIX = {'HTTP Links'}
    BEAR_DEPS = {URLHeadBear}
    HTTPS_PREFIX = 'https'
    HTTP_PREFIX = 'http'

    def run(self, filename, file, dependency_results=dict(),
            network_timeout: typed_dict(str, int, DEFAULT_TIMEOUT) = dict()):
        """
        Find http links in any text file and check if the https version of
        link is valid. If so, an option is provided for replacing them with
        https.

        An https link is considered valid if the server responds with a 2xx
        code.

        Warning: This bear will make HEAD requests to all URLs mentioned in
        your codebase, which can potentially be destructive. As an example,
        this bear would naively just visit the URL from a line that goes like
        `do_not_ever_open = 'https://api.acme.inc/delete-all-data'` wiping out
        all your data.

        :param network_timeout:       A dict mapping URLs and timeout to be
                                      used for that URL. All the URLs that have
                                      the same host as that of URLs provided
                                      will be passed that timeout. It can also
                                      contain a wildcard timeout entry with key
                                      '*'. The timeout of all the websites not
                                      in the dict will be the value of the key
                                      '*'.
        """
        for result in dependency_results.get(URLHeadBear.name, []):
            line_number, link, code, context = result.contents
            if link.startswith(self.HTTPS_PREFIX):
                continue

            https_link = self.HTTPS_PREFIX + link[len(self.HTTP_PREFIX):]
            host = urlparse(https_link).netloc
            network_timeout = {
                urlparse(url).netloc if not url == '*' else '*': timeout
                for url, timeout in network_timeout.items()}
            https_response = URLHeadBear.get_head_response(
                https_link,
                network_timeout.get(host)
                if host in network_timeout
                else network_timeout.get('*')
                if '*' in network_timeout
                else HTTPSBear.DEFAULT_TIMEOUT)

            try:
                https_code = https_response.status_code
            except AttributeError:
                continue

            if not https_code or not 200 <= https_code < 300:
                continue

            diff = Diff(file)
            current_line = file[line_number - 1]
            start = current_line.find(link)
            end = start + len(link)
            replacement = (current_line[:start] + 'https' +
                           link[len(self.HTTP_PREFIX):] + current_line[end:])
            diff.change_line(line_number, current_line, replacement)

            yield Result.from_values(
                origin=self,
                message='https can be used instead of http',
                diffs={filename: diff},
                file=filename,
                line=line_number,
                severity=RESULT_SEVERITY.NORMAL)
