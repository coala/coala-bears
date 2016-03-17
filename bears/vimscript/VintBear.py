import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class VintBear(LocalBear, Lint):
    executable = 'vint'
    output_regex = re.compile(
        r'(?P<filename>.+):(?P<line>\d+):'
        r'(?P<column>\d+): (?P<message>.+)')

    def run(self, filename, file):
        '''
        Checks the code with ``vint-linter``.
        '''
        self.arguments = '{filename}'
        return self.lint(filename)
