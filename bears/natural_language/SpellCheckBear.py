from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.PipRequirement import PipRequirement


@linter(executable='scspell',
        use_stderr=True,
        output_format='regex',
        output_regex=r'(?P<filename>.*):(?P<line>.\d*):\s*(?P<message>.*)')
class SpellCheckBear:
    """
    Lints files to check for incorrect spellings using ``scspell``.

    See <https://pypi.python.org/pypi/scspell3k> for more information.
    """
    LANGUAGES = {'Natural Language'}
    REQUIREMENTS = {PipRequirement('scspell3k', '2.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/87753'
    CAN_DETECT = {'Spelling'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--report-only', filename
