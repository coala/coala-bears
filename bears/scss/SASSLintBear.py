import json
import os

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


@linter(executable='sass-lint')
class SASSLintBear:
    """
    Check SCSS/SASS code to keep it clean and readable.
    """

    LANGUAGES = {'SCSS', 'SASS'}
    REQUIREMENTS = {NpmRequirement('sass-lint', '1.12.1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting'}
    SEE_MORE = 'https://github.com/sasstools/sass-lint'

    severity_map = {2: RESULT_SEVERITY.MAJOR,
                    1: RESULT_SEVERITY.NORMAL,
                    0: RESULT_SEVERITY.INFO}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         sasslint_config: str = ''):
        """
        :param sasslint_config: The location of the sass-lint config file.
        """
        args = tuple()
        if os.path.splitext(filename)[1] == '.scss':
            args += ('--syntax=scss',)
        if sasslint_config:
            args += ('--config=' + sasslint_config,)
        args += ('--format=json', '--verbose', '--no-exit', filename)
        return args

    def process_output(self, output, filename, file):
        if not output:  # backwards compatible no results
            return

        output = json.loads(output)

        for result in output[0]['messages']:
            origin = (
                '{class_name} ({rule})'.format(class_name=type(self).__name__,
                                               rule=result['ruleId'])
                if result['ruleId'] is not None else self)
            yield Result.from_values(
                origin=origin, message=result['message'],
                file=filename, line=result['line'], diffs=None,
                severity=self.severity_map[result['severity']])
