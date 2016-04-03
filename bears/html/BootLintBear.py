from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Setting import typed_list


@linter(executable='bootlint',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d*):(?P<column>\d*) (?P<severity>.)\d+ '
                     r'(?P<message>.+)',
        severity_map={"W": RESULT_SEVERITY.NORMAL,
                      "E": RESULT_SEVERITY.MAJOR})
class BootLintBear:
    """
    Checks the code with ``bootlint`` on each file separately.
    """

    @staticmethod
    def create_arguments(filename, file, config_file,
                         bootlint_ignore: typed_list(str)=[]):
        """
        :param bootlint_ignore: List of checkers to ignore.
        """
        ignore = ','.join(part.strip() for part in bootlint_ignore)
        return '--disable=' + ignore, filename
