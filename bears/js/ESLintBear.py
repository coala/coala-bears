import json

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement
from coalib.results.Diff import Diff
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


@linter(executable='eslint',
        use_stdin=True,
        use_stderr=True)
class ESLintBear:
    """
    Check JavaScript and JSX code for style issues and semantic errors.

    Find out more at <http://eslint.org/docs/rules/>.
    """

    LANGUAGES = {'JavaScript', 'JSX'}
    REQUIREMENTS = {NpmRequirement('eslint', '2'),
                    NpmRequirement('babel-eslint', '6'),
                    NpmRequirement('eslint-plugin-import', '1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/38739'
    CAN_DETECT = {'Syntax'}
    CAN_FIX = {'Formatting'}

    severity_map = {2: RESULT_SEVERITY.MAJOR,
                    1: RESULT_SEVERITY.NORMAL,
                    0: RESULT_SEVERITY.INFO}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         eslint_config: str=''):
        """
        :param eslint_config: The location of the .eslintrc config file.
        """
        args = (
            '--no-ignore',
            '--no-color',
            '-f=json',
            '--stdin',
            '--stdin-filename=' + filename,
        )

        if eslint_config:
            args += ('--config', eslint_config)
        else:
            args += ('--config', config_file)

        return args

    @staticmethod
    def generate_config(filename, file):
        return '{"extends": "eslint:recommended"}'

    def process_output(self, output, filename, file):
        if output[1]:
            self.warn('While running {0}, some issues were found:'
                      .format(self.__class__.__name__))
            self.warn(output[1])

        if not file or not output[0]:
            return

        output = json.loads(output[0])
        lines = ''.join(file)

        assert len(output) == 1

        for result in output[0]['messages']:
            if 'fix' not in result:
                diffs = None
            else:
                fix = result['fix']
                start, end = fix['range']
                replacement_text = fix['text']
                new_output = lines[:start] + replacement_text + lines[end:]
                diffs = {filename: Diff.from_string_arrays(
                    lines.splitlines(True), new_output.splitlines(True))}

            origin = (
                '{class_name} ({rule})'.format(class_name=type(self).__name__,
                                               rule=result['ruleId'])
                if result['ruleId'] is not None else self)
            yield Result.from_values(
                origin=origin, message=result['message'],
                file=filename, line=result['line'], diffs=diffs,
                severity=self.severity_map[result['severity']])
