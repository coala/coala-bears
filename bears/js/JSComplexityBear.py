import json

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result


class JSComplexityBear(LocalBear, Lint):
    executable = "cr"
    LANGUAGES = "Javascript"

    def process_output(self, output, filename, file):
        message = "{} has a cyclomatic complexity of {}."
        if output:
            output = json.loads("".join(output))
            for function in output["reports"][0]["functions"]:
                if function["cyclomatic"] >= self.cc_threshold:
                    yield Result.from_values(
                        origin=self,
                        message=message.format(function["name"],
                                               function["cyclomatic"]),
                        file=filename,
                        line=function["line"])

    def run(self,
            filename,
            file,
            cc_threshold: int=10):
        """
        Calculates cyclomatic complexity using ``cr``.

        :param cc_threshold: Threshold value for cyclomatic complexity
        """
        self.cc_threshold = cc_threshold
        self.arguments = "--format json {filename}"
        return self.lint(filename, file)
