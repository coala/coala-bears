import re

from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class coalaBear(LocalBear):
    LANGUAGES = {'All'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/4p1i873ebi9qdfmczn2tvxrm0'
    CAN_DETECT = {'Spelling'}

    def run(self, filename, file):
        """
        Check for the correct spelling of ``coala`` in the file.
        """
        corrected = []
        for line in file:
            wrong_spelling = r'C([oO][aA][lL][aA])'
            corrected += [re.sub(wrong_spelling,
                                 lambda match: 'c' + match.group(1),
                                 line)]
        diffs = Diff.from_string_arrays(file, corrected).split_diff()
        for diff in diffs:
            yield Result(self,
                         '``coala`` is always written with a lower case ``c``',
                         affected_code=(diff.range(filename),),
                         diffs={filename: diff},
                         severity=RESULT_SEVERITY.MAJOR)
