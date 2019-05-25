import json

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement
from coalib.results.Diff import Diff
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result
from coalib.settings.Setting import typed_list
from coalib.settings.Setting import language


@linter(executable='eslint',
        use_stdin=True,
        use_stderr=True)
class ESLintBear:
    """
    Check JavaScript and JSX code for style issues and semantic errors.

    Find out more at <http://eslint.org/docs/rules/>.
    """

    LANGUAGES = {'JavaScript', 'JSX', 'Markdown', 'Typescript', 'HTML'}
    REQUIREMENTS = {NpmRequirement('eslint', '3'),
                    NpmRequirement('babel-eslint', '8.0'),
                    NpmRequirement('eslint-plugin-import', '2'),
                    NpmRequirement('typescript-eslint-parser', '12.0.0'),
                    NpmRequirement('eslint-plugin-typescript', '0.8.1'),
                    NpmRequirement('eslint-plugin-markdown', '1.0.0-beta.6'),
                    NpmRequirement('eslint-plugin-html', '3.2.2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/38739'
    CAN_DETECT = {'Syntax'}
    CAN_FIX = {'Formatting'}

    severity_map = {2: RESULT_SEVERITY.MAJOR,
                    1: RESULT_SEVERITY.NORMAL,
                    0: RESULT_SEVERITY.INFO}

    def create_arguments(self, filename, file, config_file,
                         eslint_config: str = '',
                         language: language = language('JavaScript'),
                         global_vars: typed_list(str) = (),
                         eslint_env: typed_list(str) = (),
                         ):
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

        if 'Markdown' in language:
            args += ('--plugin', 'markdown',)
        elif 'Typescript' in language:
            args += ('--parser', 'typescript-eslint-parser',
                     '--plugin', 'typescript')
        elif 'HTML' in language:
            args += ('--plugin', 'html')
        elif 'Javascript' not in language:
            self.err(
                'Language needs to be either Markdown, HTML, TypeScript '
                'or JavaScript. Assuming JavaScript.')

        if eslint_env:
            for env in eslint_env:
                args += ('--env', env)
        if global_vars:
            for var in global_vars:
                args += ('--global', var)

        if eslint_config:
            args += ('--config', eslint_config)
        else:
            args += ('--config', config_file)

        return args

    @staticmethod
    def generate_config(filename, file):
        return '{"extends": "eslint:recommended"}'

    def process_output(self, output, filename, file):
        def warn_issue(message):
            self.warn('While running {0}, some issues were found:'
                      .format(self.__class__.__name__))
            self.warn(message)

        # Taking output from stderr for ESLint 2 program errors.
        # ESLint 2 is no longer supported, but it is here so that anyone
        # with ESLint 2 will still see any errors that were emitted.
        if output[1]:
            warn_issue(output[1])

        if not file or not output[0]:
            return

        # Handling program errors
        # such as malformed config file or missing plugin
        # that are not in json format.
        try:
            output = json.loads(output[0])
        except ValueError:
            warn_issue(output[0])
            return

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
                if result.get('ruleId') is not None else self)
            yield Result.from_values(
                origin=origin, message=result['message'],
                file=filename, line=result.get('line'), diffs=diffs,
                severity=self.severity_map[result['severity']])
