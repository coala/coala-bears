from shutil import which

import re

from coalib.bearlib.abstractions.Linter import linter
from coalib.misc.Shell import run_shell_command
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange


@linter(executable='mix', use_stdout=True,
        use_stderr=True)
class CredoBear:
    """
    Uses Credo a static code analysis tool to lint
    Elixir code and check for refactoring opportunities,
    dupicated code fragments and inconsistencies in
    naming scheme.
    """
    LANGUAGES = {'Elixir'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Complexity',
                  'Documentation',
                  'Duplicated',
                  'Formatting',
                  'Readability',
                  'Unused Code'}
    severity_map = {'C': RESULT_SEVERITY.MAJOR,
                    'D': RESULT_SEVERITY.INFO,
                    'F': RESULT_SEVERITY.INFO,
                    'R': RESULT_SEVERITY.NORMAL,
                    'W': RESULT_SEVERITY.MAJOR}
    SEE_MORE = 'http://credo-ci.org/'

    @classmethod
    def check_prerequisites(cls):  # pragma: no cover
        """
        Checks if ``mix`` is installed
        :return:
        ``True`` if ``mix`` is installed otherwise False
        """
        if which('mix') is None:
            return ('mix is not installed. Make sure to install it from '
                    'http://elixir-lang.org/install.html')

    @classmethod
    def check_credo(cls):  # pragma: no cover
        """
        Executes ``mix credo`` to ensure that ``credo`` is installed as a
        dependency.

        :return:
        ``True`` if ``credo`` is installed as a depenedency,
        otherwise ``False``
        """
        arguments = ('mix', 'credo')
        stdout_output, _ = run_shell_command(arguments)
        if stdout_output is None:
            return False
        else:
            return True

    def process_output():
        message_map = {'C': 'Found consistency issue',
                       'D': 'Found software design issue',
                       'F': 'Found refactoring opportunity',
                       'R': 'Found readability issue',
                       'W': 'Found a warning, please take a closer look'}

        exp = re.compile('(?P<issue>.*):'
                         '(?P<severity>[CDFRW]): (?P<message>.*)')

        for paragraph in output:
            if paragraph:
                suggestions = paragraph.split('\n')
        suggestions = [line for line in suggestions if line.strip()]

        for suggestion in suggestions:
            match = re.search(exp, suggestion)
            issue = match.group('issue').split(':')

        file_name = issue[0]
        line = int(issue[1])

        try:
            column = int(issue[2])
        except IndexError:
            column = 0

        severity = match.group('severity')
        msg = match.group('message')

        affected_code = list()
        affected_code.append(
            SourceRange.from_values(file_name,
                                    start_line=line,
                                    start_column=column))

        yield Result(
                self, message_map[severity],
                affected_code, severity_map[severity],
                additional_info=(msg))

    @staticmethod
    def create_arguments(self, filename, file, config_file,
                         lintmode: str = 'flycheck'):
        if lintmode:
            return ('credo', '--strict', '--format=', lintmode, filename)
        else:
            return ('credo', '--strict', '--format=flycheck', filename)
