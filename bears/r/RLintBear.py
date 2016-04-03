from coalib.bearlib.abstractions.Linter import linter

from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='Rscript',
        output_format='regex',
        output_regex=r'.*?:(?P<line>\d+):(?P<column>\d+): '
                     r'(?P<severity>\S+): (?P<message>.*)',
        severity_map={"style": RESULT_SEVERITY.NORMAL,
                      "warning": RESULT_SEVERITY.NORMAL,
                      "error": RESULT_SEVERITY.MAJOR},
        prerequisite_check_command=('Rscript', '-e', 'library(lintr)'),
        prerequisite_check_fail_message='R library "lintr" is not installed.')
class RLintBear:
    """
    Checks the code with ``lintr``.
    """
    LANGUAGES = "R"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '-e', 'library(lintr)', '-e', 'lintr::lint(' + filename + ')'
