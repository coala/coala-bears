import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class SQLintBear(LocalBear, Lint):
    executable = 'sqlint'
    output_regex = re.compile(
        r'(?P<file_name>.+?):(?P<line>\d+):(?P<column>\d+):'
        r'(?P<severity>ERROR|WARNING) (?P<message>.+(?:\r?\n  .+)*)')
    use_stdin = True
    severity_map = {
        "WARNING": RESULT_SEVERITY.NORMAL,
        "ERROR": RESULT_SEVERITY.MAJOR
    }

    def run(self, filename, file):
        '''
        Checks the given file using `sqlint`.
        '''
        return self.lint(filename, file)
