import json
import re

from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.NpmRequirement import NpmRequirement
from coalib.misc.Compatibility import JSONDecodeError
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


@linter(executable='cr')
class JSComplexityBear:
    """
    Calculates cyclomatic complexity using ``cr``, the command line utility
    provided by the NodeJS module ``complexity-report``.
    """

    LANGUAGES = {"JavaScript"}
    REQUIREMENTS = {NpmRequirement('complexity-report', '2.0.0-alpha')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/39250'
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
            try:
                output = json.loads(output)
            except JSONDecodeError:
                output_regex = (r'Fatal error \[getReports\]: .+: '
                                r'Line (?P<line>\d+): (?P<message>.*)')
                for match in re.finditer(output_regex, output):
                    groups = match.groupdict()
                    yield Result.from_values(
                        origin=self,
                        message=groups["message"].strip(),
                        file=filename,
                        severity=RESULT_SEVERITY.MAJOR,
                        line=int(groups["line"]))
                return
            for function in output["reports"][0]["functions"]:
                if function["cyclomatic"] >= cc_threshold:
                    yield Result.from_values(
                        origin=self,
                        message=message.format(function["name"],
                                               function["cyclomatic"]),
                        file=filename,
                        line=function["line"])
