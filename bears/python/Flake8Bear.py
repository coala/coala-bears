from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.bears.requirements.PipRequirement import PipRequirement


@linter(executable='flake8',
        output_format='regex',
        output_regex=r'(?P<filename>.*):(?P<line>\d+):(?P<column>\d+):\s'
                     r'(?P<severity>[EFW]|C9|N8)[0-9]{2,3}\s'
                     r'(?P<message>.*)',
        severity_map={
            "F": RESULT_SEVERITY.MAJOR,
            "E": RESULT_SEVERITY.MAJOR,
            "W": RESULT_SEVERITY.NORMAL,
            "N8": RESULT_SEVERITY.INFO,
            "C9": RESULT_SEVERITY.INFO})
class Flake8Bear:
    """
    Checks for styling errors based on pep8, pyflakes, pycodestyle and mccabe.

    See <https://gitlab.com/pycqa/flake8> for more information
    """
    LANGUAGES = {"Python 3"}
    REQUIREMENTS = {PipRequirement('flake8', '3.*')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/06mjx6o5idamjggv71gr5n1o2'
    CAN_DETECT = {'Styling checks and unused imports'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ('--hang-closing', '--disable-noqa', '--isolated',
                '--doctests', filename)
