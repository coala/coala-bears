import eradicate

from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result


class PyCommentedCodeBear(LocalBear):

    def run(self, filename, file):
        """
        Detects commented out source code in Python.
        """
        corrected = list(eradicate.filter_commented_out_code(''.join(file)))

        for diff in Diff.from_string_arrays(file, corrected).split_diff():
            yield Result(self,
                         "This file contains commented out source code.",
                         affected_code=(diff.range(filename),),
                         diffs={filename: diff})
