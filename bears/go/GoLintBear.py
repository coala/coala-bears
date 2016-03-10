import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class GoLintBear(LocalBear, Lint):
    executable = 'golint'
    output_regex = re.compile(
            r'(?P<path>.*?)\:(?P<line>\d+)\:(?P<column>\d+)\: (?P<message>.*)')

    def run(self,
            filename,
            file,
            golint_cli_options: str=""):
        '''
        Checks the code using `golint`. This will run golint over each file
        seperately.

        :param golint_cli_options: Any other flags you wish to pass to golint
                                   can be passed.
        '''
        arguments = (filename,)
        if golint_cli_options:
            arguments = (golint_cli_options,) + arguments

        return self.lint(arguments)
