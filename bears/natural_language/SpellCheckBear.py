from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement


@linter(executable='scspell',
        use_stderr=True,
        output_format='regex',
        output_regex=r'.*:(?P<line>.\d*):\s*(?P<message>.*)')
class SpellCheckBear:
    """
    Lints files to check for incorrect spellings using ``scspell``.

    scspell is a spell checker for source code.
    When applied to a code written in most popular programming languages
    while using most typical naming conventions, this algorithm will
    usually catch many errors without an annoying false positive rate.

    In an effort to catch more spelling errors, scspell is able to
    check each file against a set of dictionary words selected
    specifically for that file.

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
