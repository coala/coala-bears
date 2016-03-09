import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from bears.CheckPrerequisites import check_linter_prerequisites_builder


class RubyLinterBear(LocalBear, Lint):
    executable = 'ruby'
    arguments = '-S ruby-lint {filename}'
    output_regex = re.compile(
        r'^.+?: (?:(?P<severity>warning|error)): '
        r'line (?P<line>\d+), column (?P<column>\d+): '
        r'(?P<message>.+)')
    check_prerequisites = classmethod(
                        check_linter_prerequisites_builder(
                            executable,
                            ["ruby", "-S", "ruby-lint", '{filename}'],
                            "invalid ruby file"
                            )
                        )
    severity_map = {
        "warning": RESULT_SEVERITY.NORMAL,
        "error": RESULT_SEVERITY.MAJOR}

    def run(self, filename, file):
        '''
        Checks the code with `ruby-lint` on each file separately.
        '''
        return self.lint(filename)
