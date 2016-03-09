import json

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.misc.Shell import escape_path_argument
from coalib.results.Result import Result


class ESLintBear(LocalBear, Lint):
    executable = 'eslint'
    severity_map = {
        2: RESULT_SEVERITY.MAJOR,
        1: RESULT_SEVERITY.NORMAL,
        0: RESULT_SEVERITY.INFO
    }
    use_stdin = True
    gives_corrected = True

    def run(self, filename, file, eslint_config: str=""):
        '''
        Checks the code with eslint. This will run eslint over each of the files
        seperately.

        :param eslint_config: The location of the .eslintrc config file.
        '''
        self.arguments = '--no-ignore --no-color -f=json --stdin'
        if eslint_config:
            self.arguments += (" --config "
                               + escape_path_argument(eslint_config))

        return self.lint(filename, file)

    def _process_corrected(self, output, filename, file):
        output = json.loads("".join(output))
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

            yield Result.from_values(
                origin="{class_name} ({rule})".format(
                    class_name=self.__class__.__name__, rule=result['ruleId']),
                message=result['message'],
                file=filename,
                diffs=diffs,
                severity=self.severity_map[result['severity']],
                line=result['line'])
