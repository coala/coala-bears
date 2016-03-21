import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class GoErrCheckBear(LocalBear, Lint):
    executable = 'errcheck'
    arguments = "{filename}"
    output_regex = re.compile(r'(?P<file_name>.*go):\s*'
                              r'(?P<line>\d+):(?P<column>\d+)\s*'
                              r'(?P<message>.*)')
    use_stderr = True

    def run(self, filename, file):
        '''
        Checks the code using `errcheck`. This will run errcheck over each file
        seperately.
        '''
        return self.lint(filename)
