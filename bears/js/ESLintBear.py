import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.results.Diff import Diff
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


@linter(executable='eslint',
        use_stdin=True)
class ESLintBear:
    """
    Check JavaScript and JSX code for style issues and semantic errors.

    Find out more at <http://eslint.org/docs/rules/>.
    """

    LANGUAGES = ("JavaScript", "JSX")

    severity_map = {2: RESULT_SEVERITY.MAJOR,
                    1: RESULT_SEVERITY.NORMAL,
                    0: RESULT_SEVERITY.INFO}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         eslint_config: str=""):
        """
        :param eslint_config: The location of the .eslintrc config file.
        """
        args = '--no-ignore', '--no-color', '-f=json', '--stdin'
        if eslint_config:
            args += ('--config', eslint_config)
        return args

    def process_output(self, output, filename, file):
        output = json.loads(output)
        lines = "".join(file)

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
                "{class_name} ({rule})".format(class_name=type(self).__name__,
                                               rule=result['ruleId'])
                if result['ruleId'] is not None else self)
            yield Result.from_values(
                origin=origin, message=result['message'],
                file=filename, line=result['line'], diffs=diffs,
                severity=self.severity_map[result['severity']])
