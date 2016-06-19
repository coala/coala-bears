import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.NpmRequirement import NpmRequirement
from coalib.results.Result import Result


@linter(executable='cr')
class JSComplexityBear:
    """
    Calculates cyclomatic complexity using ``cr``.
    """
    LANGUAGES = {"JavaScript"}
    REQUIREMENTS = {NpmRequirement('complexity-report', '2.0.0-alpha')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Complexity'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--format', 'json', filename

    def process_output(self, output, filename, file, cc_threshold: int=10):
        """
        :param cc_threshold: Threshold value for cyclomatic complexity
        """
        message = "{} has a cyclomatic complexity of {}."
        if output:
            output = json.loads(output)
            for function in output["reports"][0]["functions"]:
                if function["cyclomatic"] >= cc_threshold:
                    yield Result.from_values(
                        origin=self,
                        message=message.format(function["name"],
                                               function["cyclomatic"]),
                        file=filename,
                        line=function["line"])
