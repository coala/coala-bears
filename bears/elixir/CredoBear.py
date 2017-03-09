from shutil import which

import re

from coalib.bearlib.abstractions.Linter import linter
from coalib.misc.Shell import run_shell_command
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange


@linter(executable='mix',
        use_stdout=True,
        use_stderr=True)
class CredoBear:

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

    @classmethod
    def check_prerequisites(cls):  # pragma: no cover
        if which('bash') is None:
            return 'bash is not installed.'
        if which('mix') is None:
            return ('mix is not installed. Make sure to install it from '
                    'http://elixir-lang.org/install.html')
        if cls.credo_available() is False:
            return ('credo is not installed. Make sure to install it from '
                    'https://github.com/rrrene/credo')
        else:
            return True

    @classmethod
    def credo_available(cls):  # pragma: no cover
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

    def process_output(self, output, filename, file):
        """
        Analyze Elixir code with ``credo`` get suggestions for improvements,
        such as keeping a consistent code style, increase code readability,
        opportunities to refactor code, consistency issues such as missing
        calls to ``IEx.pry`` during a debugging session, warnings about
        duplicated code.
        """
        exp = re.compile(
                    '(?P<issue>.*): (?P<severity>[CDFRW]): (?P<message>.*)')

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
            if (severity == 'C'):
                yield Result(
                    self, 'Found consistency issue.',
                    affected_code, RESULT_SEVERITY.MAJOR,
                    additional_info=(msg))
            if (severity == 'D'):
                yield Result(
                    self, 'Found software design issue.',
                    affected_code, RESULT_SEVERITY.INFO,
                    additional_info=(msg))
            if (severity == 'F'):
                yield Result(
                    self, 'Found refactoring opportunity.',
                    affected_code, RESULT_SEVERITY.INFO,
                    additional_info=(msg))
            if (severity == 'R'):
                yield Result(
                    self, 'Found readability issue.',
                    affected_code, RESULT_SEVERITY.NORMAL,
                    additional_info=(msg))
            if (severity == 'W'):
                yield Result(
                    self, 'Found a warning please take a closer look.',
                    affected_code, RESULT_SEVERITY.MAJOR,
                    additional_info=(msg))

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ('credo', '--strict', '--format=flycheck', filename)
