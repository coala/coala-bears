import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class CPPCleanBear(LocalBear, Lint):
    executable = 'cppclean'
    output_regex = re.compile(
        r'(?P<file_name>[^,:]+):(?P<line>\d+):(?P<message>.*)')
    use_stdout = True
    arguments = '{filename}'

    def run(self, filename, file):
        '''
        Checks code with `cppclean`.
        '''
        return self.lint(filename)
