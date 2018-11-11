from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result


class PyStringConcatBear(LocalBear):
    LANGUAGES = {'Python', 'Python 2', 'Python 3'}
    CAN_DETECT = {'Formatting'}

    def run(self, filename, file):
        """
        Detects use of explicit string concatenation in Python using `+`, which
        should be avoided.

        :param filename:
            Name of the file that needs to be checked.
        :param file:
            File that needs to be checked in the form of a list of strings.
        """
        string_enclosings = ['\"', '`', '\'']

        for line_number, line in enumerate(file):
            if len(line.strip()) > 0:
                if line[-2:-1] in '+':
                    next_line = file[line_number+1]
                    first_char = len(next_line) - len(next_line.lstrip())

                    if next_line[first_char] in string_enclosings:
                        yield Result.from_values(
                            origin=self,
                            message='Use of explicit string concatenation with '
                            '`+` should be avoided.',
                            file=filename,
                            line=line_number + 1,
                            column=len(line) - 1,
                            end_line=line_number + 2,
                            end_column=len(line)
                            )
