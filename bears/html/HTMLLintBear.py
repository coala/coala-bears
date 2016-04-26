from shutil import which
import sys

from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import typed_list


@linter(executable=sys.executable,
        output_format='regex',
        output_regex=r'(?P<line>\d+):(?P<column>\d+): '
                     r'(?P<severity>Error|Warning|Info): (?P<message>.+)')
class HTMLLintBear:
    """
    Check HTML source code for invalid or misformatted code.

    See also <https://pypi.python.org/pypi/html-linter>.
    """

    _html_lint = which('html_lint.py')

    LANGUAGES = "HTML"

    @staticmethod
    def create_arguments(filename, file, config_file,
                         htmllint_ignore: typed_list(str)=()):
        """
        :param htmllint_ignore: List of checkers to ignore.
        """
        ignore = ','.join(part.strip() for part in htmllint_ignore)
        return HTMLLintBear._html_lint, '--disable=' + ignore, filename
