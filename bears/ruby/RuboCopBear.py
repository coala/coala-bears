import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class RuboCopBear(LocalBear, Lint):
    executable = 'ruby'
    arguments = '-S rubocop --format emacs {filename}'
    prerequisite_command = executable + arguments
    prerequisite_fail_msg = 'rubocop not found'
    output_regex = re.compile(
        r'(?P<file_name>.+):\s*(?P<line>\d+):(?P<column>\d+):\s*'
        r'(?P<severity>[RCW]|[CF]:)\s*(?P<message>.*)')
    severity_map = {
        "E": RESULT_SEVERITY.MAJOR,
        "F": RESULT_SEVERITY.MAJOR,
        "W": RESULT_SEVERITY.NORMAL,
        "C": RESULT_SEVERITY.NORMAL,
        "R": RESULT_SEVERITY.NORMAL
        }

    def run(self, filename, file):
        '''
        Checks the code with `rubocop` on each file separately.
        '''
        return self.lint(filename)
