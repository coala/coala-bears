from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class LineCountBear(LocalBear):

    def run(self, filename, file, max_lines_per_file: int):
        """
        Checks that files are smaller than a given size.

        :param max_lines_per_file: Number of lines allowed per file.
        """
        if len(file) > max_lines_per_file:
            yield Result.from_values(
                origin=self,
                message="This file has {count} lines.".format(count=len(file)),
                severity=RESULT_SEVERITY.NORMAL,
                file=filename)
