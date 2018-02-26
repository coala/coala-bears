import re

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result


class LicenseHeaderBear(LocalBear):
    """
    Checks for copyright notice in a file.
    """
    LANGUAGES = {'All'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'License'}

    def run(self, filename, file,
            author_name: str = ''):
        """
        :param author: pass the name of the author
        """
        copyright_regexp = \
            r'Copyright\s+(\(C\)\s+)?\d{4}([-,]\d{4})*\s+%(author)s'
        re_copyright = re.compile(copyright_regexp %
                                  {'author': author_name}, re.IGNORECASE)
        if not(re_copyright.search(''.join(file))):
            message = 'Copyright notice not present.'
            re_copyright = re.compile(copyright_regexp %
                                      {'author': ''}, re.IGNORECASE)
            if author_name and re_copyright.search(''.join(file)):
                yield Result.from_values(self,
                                         'Copyright notice '
                                         'with different/no author present.',
                                         file=filename)
            else:
                yield Result.from_values(self, message, file=filename)
