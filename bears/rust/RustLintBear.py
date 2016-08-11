from coalib.bearlib.abstractions.Linter import linter


@linter(executable='rustc',
        output_format='regex',
        use_stderr=True,
        prerequisite_check_command=('rustc', '--version'),
        prerequisite_check_fail_message='rustc is not installed.',
        output_regex=r'(?P<file>.+?):(?P<line>\d+):(?P<col>\d+):\s+\d+:\d+\s'
                     r'(?:(?P<error>(error|fatal error))|'
                     r'(?P<warning>warning)):\s+(?P<message>.+)')
class RustLintBear:
    """
    This bear checks ``rust`` code for syntax and formatting issues using
    ``rustc`` utility.
    """
    LANGUAGES = {"Rust"}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/82522'
    CAN_FIX = {'Formatting', 'Syntax', 'Unused Code'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '-Zno-trans', filename,
