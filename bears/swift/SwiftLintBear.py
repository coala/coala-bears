import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.misc.Shell import escape_path_argument
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class SwiftLintBear(LocalBear, Lint):
    executable = 'swiftlint'
    use_stdin = True
    use_stdout = True
    output_regex = re.compile(
        r'<nopath>:(?P<line>\d+):(?P<column>\d+)?:? '
        r'(?P<severity>error|warning): '
        r'(?P<message>.+)'
    )
    severity_map = {
        "error": RESULT_SEVERITY.MAJOR,
        "warning": RESULT_SEVERITY.NORMAL
    }

    def run(self, filename, file):
        '''
        Checks the code with swiftlint. This will run swiftlint over
        each file seperately.
        '''
        self.arguments = 'lint --use-stdin'
        self.lint(filename, file)