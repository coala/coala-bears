import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class VintBear(LocalBear, Lint):
    executable = 'vint'
    arguments = '{filename}'
    output_regex = re.compile(
        r'(?P<filename>.+):(?P<line>\d+):'
        r'(?P<column>\d+): (?P<message>.+)')

    def run(self, filename, file):
        '''
        Checks vimscript code for possible problems using ``vint-linter``.
        '''
        return self.lint(filename)
