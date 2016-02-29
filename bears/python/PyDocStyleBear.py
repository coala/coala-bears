from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class PyDocStyleBear(LocalBear, Lint):
    executable = 'pydocstyle'
    arguments = '{filename}'
    output_regex = r'(.*\.py):(?P<line>\d+) (.+):\n\s+(?P<message>.*)'
    use_stderr = True

    def run(self, filename, file):
        '''
        Checks python docstrings.
        '''
        return self.lint(filename, file)
