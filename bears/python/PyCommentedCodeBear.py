import eradicate

from coalib.bears.LocalBear import LocalBear
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.results.Diff import Diff
from coalib.results.Result import Result


class PyCommentedCodeBear(LocalBear):
    LANGUAGES = {"Python", "Python 2", "Python 3"}
    REQUIREMENTS = {PipRequirement('eradicate', '0.1.*')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Commented Code'}

    def run(self, filename, file):
        """
        Detects commented out source code in Python.
        """
        corrected = tuple(eradicate.filter_commented_out_code(''.join(file)))

        for diff in Diff.from_string_arrays(file, corrected).split_diff():
            yield Result(self,
                         "This file contains commented out source code.",
                         affected_code=(diff.range(filename),),
                         diffs={filename: diff})
