import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class InferBear(LocalBear, Lint):
    executable = 'infer'
    arguments = '-npb -- javac {filename}'
    output_regex = re.compile(
        r'(?P<file_name>.+):'
        r'(?P<line>.+): '
        r'(?P<severity>error|warning): '
        r'(?P<message>.*)')
    severity_map = {
        "error": RESULT_SEVERITY.MAJOR,
        "warning": RESULT_SEVERITY.NORMAL}
    LANGUAGES = "Java"

    def run(self, filename, file):
        '''
        Checks the code with ``infer``.
        '''
        return self.lint(filename)
