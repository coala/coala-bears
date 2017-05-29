import re
import requests
from urllib.parse import urlparse
from aenum import Flag

from coalib.bears.LocalBear import LocalBear
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.bearlib import deprecate_settings
from coalib.settings.Setting import typed_list
from coalib.results.HiddenResult import HiddenResult
from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange
from coalib.parsing.Globbing import fnmatch
from coalib.settings.Setting import typed_dict
from coala_utils.decorators import (enforce_signature, generate_ordering,
                                    generate_repr)


class LINK_CONTEXT(Flag):
    no_context = 0
    xml_namespace = 1
    pip_vcs_url = 2


@generate_repr(('id', hex),
               'origin',
               'affected_code',
               'message',
               'link',
               'http_status_code',
               'link_context')
@generate_ordering('affected_code',
                   'link',
                   'http_status_code',
                   'link_context',
                   'contents',
                   'severity',
                   'confidence',
                   'origin',
                   'message_base',
                   'message_arguments',
                   'aspect',
                   'additional_info',
                   'debug_msg')
class URLResult(HiddenResult):

    @enforce_signature
    def __init__(self, origin, affected_code,
                 link: str,
                 http_status_code: (int, None),
                 link_context: LINK_CONTEXT):

        Result.__init__(self, origin,
                        '%s responds with HTTP %s' % (link, http_status_code),
                        affected_code)

        self.contents = [affected_code[0].start.line, link, http_status_code,
                         link_context]
        self.link = link
        self.http_status_code = http_status_code
        self.link_context = link_context


class URLBear(LocalBear):
    DEFAULT_TIMEOUT = 15
    LANGUAGES = {'All'}
    REQUIREMENTS = {PipRequirement('requests', '2.12'),
                    PipRequirement('aenum', '2.0.8')}
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
                ((?:%[A-Fa-f0-9][A-Fa-f0-9])*[^\s()%\'"`<>|\\\[\]]+)
                                        # Path name
                                        # This part allows precentage
                                        # encoding like %3F
                                        # and does not allow
                                        # any parenthesis: balanced or
                                        # unbalanced.
            |                           # OR
                \((?:%[A-Fa-f0-9][A-Fa-f0-9])*[^\s()%\'"`<>|\\\[\]]*\)
                                        # Path name contained within ()
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
                    link_context = LINK_CONTEXT.no_context
                    xmlns_match = xmlns_regex.search(line)
                    if xmlns_match and link in xmlns_match.groups():
                        link_context |= LINK_CONTEXT.xml_namespace
                    if link.startswith(('hg+', 'bzr+', 'git+', 'svn+')):
                        link_context |= LINK_CONTEXT.pip_vcs_url
                    file_context[link] = link_context
                if not (link_ignore_regex.search(link) or
                        fnmatch(link, link_ignore_list)):
                    yield link, line_number, link_context

    def analyze_links_in_file(self, file, network_timeout, link_ignore_regex,
                              link_ignore_list):
        for link, line_number, link_context in self.extract_links_from_file(
                file, link_ignore_regex, link_ignore_list):

            if link_context is link_context.pip_vcs_url:
                link = URLBear.parse_pip_vcs_url(link)

            host = urlparse(link).netloc
            code = URLBear.get_status_code(
                link,
                network_timeout.get(host)
                if host in network_timeout
                else network_timeout.get('*')
                if '*' in network_timeout
                else URLBear.DEFAULT_TIMEOUT)
            yield line_number + 1, link, code, link_context

    @deprecate_settings(link_ignore_regex='ignore_regex',
                        network_timeout=('timeout', lambda t: {'*': t}))
    def run(self, filename, file,
            network_timeout: typed_dict(str, int, DEFAULT_TIMEOUT)=dict(),
            link_ignore_regex: str='([.\/]example\.com|\{|\$)',
            link_ignore_list: typed_list(str)=''):
        """
        Find links in any text file.

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
        """
        network_timeout = {urlparse(url).netloc
                           if not url == '*' else '*': timeout
                           for url, timeout in network_timeout.items()}

        for line_number, link, code, context in self.analyze_links_in_file(
                file, network_timeout, link_ignore_regex, link_ignore_list):
            affected_code = SourceRange.from_values(filename, line_number)

            yield URLResult(self, (affected_code,), link, code, context)
