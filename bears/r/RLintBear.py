import re
import shutil
import subprocess

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class RLintBear(LocalBear, Lint):
    executable = 'Rscript'
    arguments = "-e 'library(lintr)' -e 'lintr::lint({filename})'"
    output_regex = re.compile(
        r'(?P<file_name>.*?):(?P<line>\d+):(?P<column>\d+):'
        r' (?P<severity>\S+): (?P<message>.*)')
    severity_map = {
        "style": RESULT_SEVERITY.NORMAL,
        "warning": RESULT_SEVERITY.NORMAL,
        "error": RESULT_SEVERITY.MAJOR}

    @classmethod
    def check_prerequisites(cls):  # pragma: no cover
        if shutil.which("Rscript") is None:
            return "R is not installed."
        else:
            try:
                subprocess.check_call(["Rscript", "-e", "library(lintr)"])
                return True
            except subprocess.CalledProcessError:
                return 'R library "lintr" is not installed.'

    def run(self, filename, file):
        '''
        Checks the code with `lintr`.
        '''
        return self.lint(filename)
