import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class LuaLintBear(LocalBear, Lint):
    executable = 'luacheck'
    output_regex = re.compile(
        r'\s*(?P<filename>.+):(?P<line>\d+):'
        r'(?P<column>\d+):\s(?P<message>.+)')

    def run(self, filename, file):
        '''
        Checks the code with ``luacheck``.
        '''
        self.arguments = '{filename}'
        return self.lint(filename)
