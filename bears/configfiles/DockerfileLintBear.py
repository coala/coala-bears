import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


@linter(executable='dockerfile_lint')
class DockerfileLintBear:
    """
    Checks the given file with ``dockerfile_lint``.
    """

    severity_map = {
        "error": RESULT_SEVERITY.MAJOR,
        "warn": RESULT_SEVERITY.NORMAL,
        "info": RESULT_SEVERITY.INFO}
    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--json', '-f', filename

    def process_output(self, output, filename, file):
        output = json.loads(output)

        for severity in output:
            if severity == "summary":
                continue
            for issue in output[severity]["data"]:
                yield Result.from_values(
                    origin=self,
                    message=issue["message"],
                    file=filename,
                    severity=self.severity_map[issue["level"]],
                    line=issue["line"])
