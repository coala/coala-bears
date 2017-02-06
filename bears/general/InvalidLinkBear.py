import re
import requests
from urllib.parse import urlparse

from difflib import SequenceMatcher

from coalib.results.Diff import Diff
from coalib.bears.LocalBear import LocalBear
from coalib.misc.Enum import enum
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result
from coalib.bearlib import deprecate_settings
from coalib.settings.Setting import typed_list
from coalib.parsing.Globbing import fnmatch
from coalib.settings.Setting import typed_dict


class InvalidLinkBear(LocalBear):
    DEFAULT_TIMEOUT = 15
    LANGUAGES = {'All'}
    REQUIREMENTS = {PipRequirement('requests', '2.12')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Documentation'}

    # IP Address of www.google.com
    check_connection_url = 'http://216.58.218.174'

    @classmethod
    def check_prerequisites(cls):
        code = cls.get_status_code(
            cls.check_connection_url, cls.DEFAULT_TIMEOUT)
        return ('You are not connected to the internet.'
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
    def parse_pip_vcs_url(link):
        splitted_at = link.split('@')[0]
        splitted_schema = splitted_at[splitted_at.index('+') + 1:]
        return splitted_schema

    @staticmethod
    def extract_links_from_file(file, link_ignore_regex, link_ignore_list):
        link_ignore_regex = re.compile(link_ignore_regex)
        regex = re.compile(
            r"""
            ((git\+|bzr\+|svn\+|hg\+|)  # For VCS URLs
            https?://                   # http:// or https:// as only these
                                        # are supported by the ``requests``
                                        # library
            [^.:%\s_/?#[\]@\\]+         # Initial part of domain
            \.                          # A required dot `.`
            (
                (?:[^\s()%\'"`<>|\\\[\]]+)  # Path name
                                            # This part does not allow
                                            # any parenthesis: balanced or
                                            # unbalanced.
            |                               # OR
                \([^\s()%\'"`<>|\\\[\]]*\)  # Path name contained within ()
                                        # This part allows path names that
                                        # are explicitly enclosed within one
                                        # set of parenthesis.
                                        # An example can be:
                                        # http://wik.org/Hello_(Adele_song)/200
            )
            *)
                                        # Thus, the whole part above
                                        # prevents matching of
                                        # Unbalanced parenthesis
            (?<!\.)(?<!,)               # Exclude trailing `.` or `,` from URL
            """, re.VERBOSE)
        file_context = {}
        for line_number, line in enumerate(file):
            xmlns_regex = re.compile(r'xmlns:?\w*="(.*)"')
            for match in re.findall(regex, line):
                link = match[0]
                link_context = file_context.get(link)
                if not link_context:
                    link_context = enum(
                        xml_namespace=False,
                        pip_vcs_url=False)
                    xmlns_match = xmlns_regex.search(line)
                    if xmlns_match and link in xmlns_match.groups():
                        link_context.xml_namespace = True
                    if link.startswith(('hg+', 'bzr+', 'git+', 'svn+')):
                        link_context.pip_vcs_url = True
                    file_context[link] = link_context
                if not (link_ignore_regex.search(link) or
                        fnmatch(link, link_ignore_list)):
                    yield link, line_number, link_context

    def analyze_links_in_file(self, file, network_timeout, link_ignore_regex,
                              link_ignore_list):
        for link, line_number, link_context in self.extract_links_from_file(
                file, link_ignore_regex, link_ignore_list):

            if link_context.pip_vcs_url:
                link = InvalidLinkBear.parse_pip_vcs_url(link)

            host = urlparse(link).netloc
            code = InvalidLinkBear.get_status_code(
                link,
                network_timeout.get(host)
                if host in network_timeout
                else network_timeout.get('*')
                if '*' in network_timeout
                else InvalidLinkBear.DEFAULT_TIMEOUT)
            yield line_number + 1, link, code, link_context

    @deprecate_settings(link_ignore_regex='ignore_regex',
                        network_timeout=('timeout', lambda t: {'*': t}))
    def run(self, filename, file,
            network_timeout: typed_dict(str, int, DEFAULT_TIMEOUT)=dict(),
            link_ignore_regex: str='([.\/]example\.com|\{|\$)',
            link_ignore_list: typed_list(str)='',
            follow_redirects: bool=False):
        """
        Find links in any text file and check if they are valid.

        A link is considered valid if the server responds with a 2xx code.

        This bear can automatically fix redirects, but ignores redirect
        URLs that have a huge difference with the original URL.

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
        :param link_ignore_regex:     A regex for urls to ignore.
        :param link_ignore_list: Comma separated url globs to ignore
        :param follow_redirects: Set to true to autocorrect redirects.
        """
        network_timeout = {urlparse(url).netloc
                           if not url == '*' else '*': timeout
                           for url, timeout in network_timeout.items()}

        for line_number, link, code, context in self.analyze_links_in_file(
                file, network_timeout, link_ignore_regex, link_ignore_list):
            if context.xml_namespace:
                if code and 200 <= code < 300:
                    pass
                else:
                    yield Result.from_values(
                        origin=self,
                        message=('XML Namespace - '
                                 '{url}').format(url=link),
                        file=filename,
                        line=line_number,
                        severity=RESULT_SEVERITY.INFO)
            elif code is None:
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
                if follow_redirects and 300 <= code < 400:  # HTTP status 30x
                    redirect_url = requests.head(link,
                                                 allow_redirects=True).url
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
                        diff.change_line(line_number,
                                         current_line,
                                         replacement)

                        yield Result.from_values(
                            self,
                            'This link redirects to ' + redirect_url,
                            diffs={filename: diff},
                            file=filename,
                            line=line_number,
                            severity=RESULT_SEVERITY.NORMAL)
