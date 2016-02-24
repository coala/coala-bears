import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class YAMLLintBear(LocalBear, Lint):
    executable = 'yamllint'
    output_regex = re.compile(
        r'(.+):(?P<line>\d+):(?P<column>\d+):\s'
        r'\[(?P<severity>error|warning)\]\s(?P<message>.+)'
    )
    severity_map = {
        "warning": RESULT_SEVERITY.NORMAL,
        "error": RESULT_SEVERITY.MAJOR
    }

    def run(self,
            filename,
            file,
            yamllint_config: str=""):
        '''
        Checks the code with `yamllint` on each file separately.

        :param yamllint_config: Path to a custom configuration file.
        '''
        arguments = ('-f', 'parsable', filename)
        if yamllint_config:
            arguments += ('--config=' + yamllint_config,)
        return self.lint(arguments)
