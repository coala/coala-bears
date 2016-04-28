from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class LineCountBear(LocalBear):
    LANGUAGES = "All"

    def run(self, filename, file, max_lines_per_file: int):
        """
        Count the number of lines in a file and ensure that they are
        smaller than a given size.

        :param max_lines_per_file: Number of lines allowed per file.
        """
        file_length = len(file)
        if file_length > max_lines_per_file:
            yield Result.from_values(
                origin=self,
                message=("This file had {count} lines, which is {extra} "
                         "lines more than the maximum limit specified."
                         .format(count=file_length,
                                 extra=file_length-max_lines_per_file)),
                severity=RESULT_SEVERITY.NORMAL,
                file=filename)
