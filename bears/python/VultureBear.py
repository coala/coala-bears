from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.PipRequirement import PipRequirement


@linter(executable='vulture',
        output_format='regex',
        output_regex=r'(?P<filename>.*):(?P<line>.*):\s*(?P<message>.*)')
class VultureBear:
    """
    Checks Python code for unused variables and functions using ``vulture``.

    See <https://bitbucket.org/jendrikseipp/vulture> for more information.
    """
    LANGUAGES = {"Python", "Python 3"}
    REQUIREMENTS = {PipRequirement('happiness', '0.10.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/82256'
    CAN_DETECT = {'Unused Code'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
