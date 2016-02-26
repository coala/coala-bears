from os.path import abspath, dirname, join
import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from bears.CheckPrerequisites import check_linter_prerequisites_builder


class CheckstyleBear(LocalBear, Lint):
    executable = 'java'
    google_checks = join(dirname(abspath(__file__)), 'google_checks.xml')
    jar = join(dirname(abspath(__file__)), 'checkstyle.jar')

    severity_map = {
        "INFO": RESULT_SEVERITY.INFO,
        "WARN": RESULT_SEVERITY.NORMAL}

    check_prerequisites = classmethod(
                        check_linter_prerequisites_builder(
                            executable,
                            ["java", "-jar", jar, "-v"],
                            "jar file {} is invalid and cannot be used".format(
                                jar)
                            )
                        )

    def run(self, filename, file):
        """
        Checks the code using `checkstyle` using the Google codestyle
        specification.
        """
        self.output_regex = re.compile(
            r'\[(?P<severity>WARN|INFO)\]\s*' + re.escape(abspath(filename)) +
            r':(?P<line>\d+)(:(?P<col>\d+))?:\s*'
            r'(?P<message>.*?)\s*\[(?P<origin>[a-zA-Z]+?)\]')
        self.arguments = '-jar ' + self.jar + ' -c ' + self.google_checks
        self.arguments += " {filename}"
        return self.lint(filename)
