import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class DartLintBear(LocalBear, Lint):
    executable = 'dartanalyzer'
    output_regex = re.compile(
        r'\[(?P<severity>error|warning)\] (?P<message>.+)\('
        r'(?P<file_name>.+), line (?P<line>\d+),'
        r' col (?P<column>\d+)\)')
    severity_map = {
        "error": RESULT_SEVERITY.MAJOR,
        "warning": RESULT_SEVERITY.NORMAL}
    LANGUAGES = "Dart"

    def run(self, filename, file):
        '''
        Checks the code with ``dart-linter``.

        This bear expects dart commands to be on your ``PATH``. Please ensure
        /path/to/dart-sdk/bin is in your ``PATH``.
        '''
        self.arguments = '{filename}'
        return self.lint(filename)
