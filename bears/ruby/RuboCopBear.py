import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


@linter(executable='rubocop',
        use_stdin=True)
class RuboCopBear:
    """
    Check Ruby code for syntactic, formatting as well as semantic problems.

    See <https://github.com/bbatsov/rubocop#cops> for more information.
    """

    LANGUAGES = "Ruby"

    severity_map = {"error": RESULT_SEVERITY.MAJOR,
                    "warning": RESULT_SEVERITY.NORMAL,
                    "convention": RESULT_SEVERITY.INFO}

    @staticmethod
    def create_arguments(filename, file, config_file):
        # Need both stdin and filename. Explained in this comment:
        # https://github.com/bbatsov/rubocop/pull/2146#issuecomment-131403694
        return filename, '--stdin', '--format=json'

    def process_output(self, output, filename, file):
        output = json.loads(output)
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
