import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class GoTypeBear(LocalBear, Lint):
    executable = 'gotype'
    arguments = "-e {filename}"
    use_stderr = True
    output_regex = re.compile(
        r'(?P<file_name>.*):(?P<line>\d+):(?P<column>\d+):\s*(?P<message>.*)')
    LANGUAGES = "Go"

    def run(self, filename, file):
        '''
        Checks the code using ``gotype``. This will run gotype over each file
        seperately.
        '''
        return self.lint(filename)
