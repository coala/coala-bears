import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class RLintBear(LocalBear, Lint):
    executable = 'Rscript'
    arguments = "-e 'library(lintr)' -e 'lintr::lint(\"{filename}\")'"
    output_regex = re.compile(
        r'(?P<file_name>.*?):(?P<line>\d+):(?P<column>\d+):'
        r' (?P<severity>\S+): (?P<message>.*)')
    severity_map = {
        "style": RESULT_SEVERITY.NORMAL,
        "warning": RESULT_SEVERITY.NORMAL,
        "error": RESULT_SEVERITY.MAJOR}
    LANGUAGES = "R"

    prerequisite_command = ["Rscript", "-e", "library(lintr)"]
    prerequisite_fail_msg = 'R library "lintr" is not installed.'

    def run(self, filename, file):
        '''
        Checks the code with `lintr`.
        '''
        return self.lint(filename)
