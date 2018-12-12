import re

from aenum import Flag
from urlextract import URLExtract

from coalib.bears.LocalBear import LocalBear
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.bearlib import deprecate_settings
from coalib.settings.Setting import typed_list
from coalib.results.HiddenResult import HiddenResult
from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange
from coalib.parsing.Globbing import fnmatch
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
               'link_context')
@generate_ordering('affected_code',
                   'link',
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
                 link_context: LINK_CONTEXT):

        Result.__init__(self, origin,
                        'Found %s with context: %s' % (link, link_context),
                        affected_code)

        self.contents = [affected_code[0].start.line, link, link_context]
        self.link = link
        self.link_context = link_context


class URLBear(LocalBear):
    LANGUAGES = {'All'}
    REQUIREMENTS = {PipRequirement('aenum', '2.0.8')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Documentation'}

    @staticmethod
    def parse_pip_vcs_url(link):
        splitted_at = link.split('@')[0]
        splitted_schema = splitted_at[splitted_at.index('+') + 1:]
        return splitted_schema

    @staticmethod
    def extract_links_from_file(file, link_ignore_regex, link_ignore_list):
        xmlns_regex = re.compile(r'xmlns:?\w*="(.*)"')
        link_ignore_regex = re.compile(link_ignore_regex)
        regex = re.compile(
            r"""
            (git\+|bzr\+|svn\+|hg\+|)  # For VCS URLs
            https?://.*                # http:// or https:// as only these
                                       # are supported by the ``requests``
                                       # library
            """, re.VERBOSE)
        file_context = {}
        extractor = URLExtract()
        for line_number, line in enumerate(file):
            if not re.findall(regex, line):
                continue
            urls = set(extractor.find_urls(line) or [])
            for url in urls:
                # URLExtract does not remove trailing `.,|\` characters
                # See https://github.com/lipoja/URLExtract/issues/13
                link = url.rstrip('.,|\\')
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

    def analyze_links_in_file(self, file, link_ignore_regex,
                              link_ignore_list):
        for link, line_number, link_context in self.extract_links_from_file(
                file, link_ignore_regex, link_ignore_list):

            if link_context is link_context.pip_vcs_url:
                link = URLBear.parse_pip_vcs_url(link)

            yield line_number + 1, link, link_context

    @deprecate_settings(link_ignore_regex='ignore_regex')
    def run(self, filename, file,
            link_ignore_regex: str = r'([.\/]example\.com|\{|\$)',
            link_ignore_list: typed_list(str) = '',
            ):
        """
        Find links in any text file.

        :param link_ignore_regex:     A regex for urls to ignore.
        :param link_ignore_list: Comma separated url globs to ignore
        """

        for (line_number, link,
             context) in self.analyze_links_in_file(
                file, link_ignore_regex, link_ignore_list):
            affected_code = SourceRange.from_values(filename, line_number)

            yield URLResult(self, (affected_code,), link, context)
