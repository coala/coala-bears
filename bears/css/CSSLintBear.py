import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class CSSLintBear(LocalBear, Lint):

    LANGUAGES = "CSS"

    executable = 'csslint'
    arguments = '--format=compact {filename}'
    output_regex = re.compile(
        r'(?P<file_name>.+):\s*'
        r'(?:line (?P<line>\d+), col (?P<col>\d+), )?'
        r'(?P<severity>Error|Warning) - (?P<message>.*)')
    severity_map = {
        "Error": RESULT_SEVERITY.MAJOR,
        "Warning": RESULT_SEVERITY.NORMAL}

    def run(self, filename, file):
        """
        Check code for syntactical or semantical problems that might lead to
        problems or inefficiencies.
        """
        return self.lint(filename)
