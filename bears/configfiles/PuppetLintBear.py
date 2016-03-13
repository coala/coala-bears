import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class PuppetLintBear(LocalBear, Lint):
    executable = 'puppet-lint'
    output_regex = re.compile(
        r'(?P<line>\d+):(?P<column>\d+):'
        r'(?P<severity>warning|error):(?P<message>.+)')
    severity_map = {
        'error': RESULT_SEVERITY.MAJOR,
        'warning': RESULT_SEVERITY.NORMAL
    }
    use_stdout = True

    def run(self, filename, file, puppet_cli_options: str=""):
        '''
        Checks the code with puppet-lint`. This will run puppet-lint
        over all puppet files seperately.
        '''
        self.arguments = '--log-format '
        self.arguments += "'%{{line}}:%{{column}}:%{{kind}}:%{{message}}'"
        if puppet_cli_options:
            self.arguments += " " + puppet_cli_options
        self.arguments += " {filename}"

        return self.lint(filename)
