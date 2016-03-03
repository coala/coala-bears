import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class ShellCheckBear(LocalBear, Lint):
    executable = 'shellcheck'
    severity_map = {
        "error": RESULT_SEVERITY.MAJOR,
        "warning": RESULT_SEVERITY.NORMAL,
        "info": RESULT_SEVERITY.INFO}
    output_regex = re.compile(
        r'(?P<file>(.+)):(?P<line>\d+):(?P<column>\d+):.'
        r'(?P<severity>error|warning|info):.(?P<message>(.+))')

    def run(self, filename, file, shell: str='sh'):
        '''
        Checks the given code with ``shellcheck``

        :param shell:  Target shell being used. Default is ``sh``.
        '''
        self.arguments = '--f gcc -s {shell} {filename}'.format(
            shell=shell, filename=filename)
        return self.lint(filename=filename)
