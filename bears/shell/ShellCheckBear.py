from coalib.bearlib.abstractions.Linter import linter


@linter(executable='shellcheck', output_format="regex",
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+): '
                     r'(?P<severity>error|warning|info): (?P<message>.+)')
class ShellCheckBear:
    """
    Check bash/shell scripts for syntactical problems (with understandable
    messages), semantical problems as well as subtle caveats and pitfalls.

    A gallery of bad code that can be detected is available at
    <https://github.com/koalaman/shellcheck/blob/master/README.md>.
    """

    LANGUAGES = {"sh", "bash", "ksh", "dash"}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Security', 'Undefined Element', 'Unused Code'}

    @staticmethod
    def create_arguments(filename, file, config_file, shell: str='sh'):
        """
        :param shell: Target shell being used.
        """
        return '--f', 'gcc', '-s', shell, filename
