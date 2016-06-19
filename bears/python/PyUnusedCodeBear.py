import autoflake

from coalib.bears.LocalBear import LocalBear
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.results.Diff import Diff
from coalib.results.Result import Result


class PyUnusedCodeBear(LocalBear):
    LANGUAGES = {"Python", "Python 2", "Python 3"}
    REQUIREMENTS = {PipRequirement('autoflake', '0.6.*')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Unused Code'}

    def run(self, filename, file):
        """
        Detects unused code. This functionality is limited to:

        - Unneeded pass statements.
        - Unneeded builtin imports. (Others might have side effects.)
        """
        corrected = autoflake.fix_code(''.join(file)).splitlines(True)

        for diff in Diff.from_string_arrays(file, corrected).split_diff():
            yield Result(self,
                         "This file contains unused source code.",
                         affected_code=(diff.range(filename),),
                         diffs={filename: diff})
