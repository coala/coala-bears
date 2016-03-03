import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Setting import typed_list


class BootLintBear(LocalBear, Lint):
    executable = 'bootlint'
    output_regex = re.compile(
        r'(.+?):*(?P<line>\d*):+'
        r'(?P<col>\d*)\s(?P<severity>.)\d+'
        r'\s(?P<message>.+)')
    severity_map = {
        "W": RESULT_SEVERITY.NORMAL,
        "E": RESULT_SEVERITY.MAJOR
    }

    def _get_groupdict(self, match):
        groups = Lint._get_groupdict(self, match)
        if groups["line"] == "" and groups["col"] == "":
            del groups["line"], groups["col"]
        return groups

    def run(self, filename, file, bootlint_ignore: typed_list(str)=[]):
        '''
        Checks the code with ``bootlint`` on each file separately.

        :param bootlint_ignore: List of checkers to ignore.
        '''
        ignore = ','.join(part.strip() for part in bootlint_ignore)
        self.arguments = '--disable=' + ignore + " {filename}"
        return self.lint(filename)
