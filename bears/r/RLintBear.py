import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class RLintBear(LocalBear, Lint):
    executable = 'Rscript'
    arguments = "-e 'library(lintr)' -e 'lintr::lint(\"{filename}\")'"
    output_regex = re.compile(
        r'(.*?):(?P<line>\d+):(?P<column>\d+):'
        r' (?P<severity>\S+): (?P<message>.*)')
    severity_map = {
        "style": RESULT_SEVERITY.NORMAL,
        "warning": RESULT_SEVERITY.NORMAL,
        "error": RESULT_SEVERITY.MAJOR}
    LANGUAGES = {"R"}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting'}

    prerequisite_command = ["Rscript", "-e", "library(lintr)"]
    prerequisite_fail_msg = 'R library "lintr" is not installed.'

    def run(self, filename, file):
        '''
        Checks the code with `lintr`.
        '''
        return self.lint(filename)
