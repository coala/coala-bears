import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.results.Result import Result


@linter(executable='cr')
class JSComplexityBear:
    """
    Calculates cyclomatic complexity using ``cr``.
    """
    LANGUAGES = "Javascript"

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
