import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class SCSSLintBear(LocalBear, Lint):
    executable = 'scss-lint'
    arguments = '{filename}'
    output_regex = re.compile(
                r'(?P<file_name>.+):(?P<line>\d+)\s*'
                r'(\[(?P<severity>.*?)\])\s*'
                r'(?P<message>.*)')
    severity_map = {
        "I": RESULT_SEVERITY.INFO,
        "W": RESULT_SEVERITY.NORMAL,
        "E": RESULT_SEVERITY.MAJOR
    }

    def run(self, filename, file):
        '''
        Checks the code with `scss-lint` on each file separately.
        '''
        return self.lint(filename)
