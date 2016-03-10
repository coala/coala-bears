import json

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


class RuboCopBear(LocalBear, Lint):
    executable = 'rubocop'
    # Need both stdin and filename. Explained in the comment:
    # https://github.com/bbatsov/rubocop/pull/2146#issuecomment-131403694
    arguments = '{filename} --stdin --format=json'
    severity_map = {
        "error": RESULT_SEVERITY.MAJOR,
        "warning": RESULT_SEVERITY.NORMAL,
        "convention": RESULT_SEVERITY.INFO
    }
    use_stdin = True

    def run(self, filename, file):
        '''
        Checks the code with ``rubocop``. This will run ``rubocop``
        over each of the files separately.
        '''
        return self.lint(filename, file)

    def _process_issues(self, output, filename):
        output = json.loads("".join(output))
        assert len(output['files']) == 1
        for result in output['files'][0]['offenses']:
            # TODO: Add condition for auto-correct, when rubocop is updated.
            # Relevant Issue: https://github.com/bbatsov/rubocop/issues/2932
            yield Result.from_values(
                origin="{class_name} ({rule})".format(
                    class_name=self.__class__.__name__,
                    rule=result['cop_name']),
                message=result['message'],
                file=filename,
                diffs=None,
                severity=self.severity_map[result['severity']],
                line=result['location']['line'],
                column=result['location']['column'],
                # Tested with linebreaks, it's secure.
                end_column=result['location']['column'] +
                result['location']['length'])
