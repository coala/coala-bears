import re
import requests

from difflib import SequenceMatcher

from coalib.results.Diff import Diff
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


class InvalidLinkBear(LocalBear):
    DEFAULT_TIMEOUT = 2
    LANGUAGES = "All"

    # IP Address of www.google.com
    check_connection_url = "http://216.58.218.174"

    @classmethod
    def check_prerequisites(cls):
        code = cls.get_status_code(
            cls.check_connection_url, cls.DEFAULT_TIMEOUT)
        return ("You are not connected to the internet."
                if code is None else True)

    @staticmethod
    def get_status_code(url, timeout):
        try:
            code = requests.head(url, allow_redirects=False,
                                 timeout=timeout).status_code
            return code
        except requests.exceptions.RequestException:
            pass

    @staticmethod
    def find_links_in_file(file, timeout, ignore_regex):
        ignore_regex = re.compile(ignore_regex)
        regex = re.compile(
            r'((ftp|http)s?:\/\/\S+\.(?:[^\s\(\)\'\"\>\|]+|'
            r'\([^\s\(\)]*\))*)(?<!\.)(?<!\,)')
        for line_number, line in enumerate(file):
            match = regex.search(line)
            if match:
                link = match.group()
                if not ignore_regex.search(link):
                    code = InvalidLinkBear.get_status_code(link, timeout)
                    yield line_number + 1, link, code

    def run(self, filename, file,
            timeout: int=DEFAULT_TIMEOUT,
            ignore_regex: str="[.\/]example\.com"):
        """
        Find links in any text file and check if they are valid.

        A link is considered valid if the server responds with a 2xx code.

        This bear can automatically fix redirects, but ignores redirect
        URLs that have a huge difference with the original URL.

        :param timeout:      Request timeout period.
        :param ignore_regex: A regex for urls to ignore.
        """
        for line_number, link, code in InvalidLinkBear.find_links_in_file(
                file, timeout, ignore_regex):
            if code is None:
                yield Result.from_values(
                    origin=self,
                    message=('Broken link - unable to connect to '
                             '{url}').format(url=link),
                    file=filename,
                    line=line_number,
                    severity=RESULT_SEVERITY.MAJOR)
            elif not 200 <= code < 300:
                # HTTP status 404, 410 or 50x
                if code in (404, 410) or 500 <= code < 600:
                    yield Result.from_values(
                        origin=self,
                        message=('Broken link - unable to connect to {url} '
                                 '(HTTP Error: {code})'
                                 ).format(url=link, code=code),
                        file=filename,
                        line=line_number,
                        severity=RESULT_SEVERITY.NORMAL)
                if 300 <= code < 400:  # HTTP status 30x
                    redirect_url = requests.head(link, allow_redirects=True).url
                    matcher = SequenceMatcher(
                        None, redirect_url, link)
                    if (matcher.real_quick_ratio() > 0.7 and
                            matcher.ratio()) > 0.7:
                        diff = Diff(file)
                        current_line = file[line_number - 1]
                        start = current_line.find(link)
                        end = start + len(link)
                        replacement = current_line[:start] + \
                            redirect_url + current_line[end:]
                        diff.change_line(line_number, current_line, replacement)

                        yield Result.from_values(
                            self,
                            'This link redirects to ' + redirect_url,
                            diffs={filename: diff},
                            file=filename,
                            line=line_number,
                            severity=RESULT_SEVERITY.NORMAL)
