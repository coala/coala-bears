from shutil import which

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(executable='elm-format',
        use_stderr=True,
        use_stdout=False,
        output_format='regex',
        output_regex=r'(?P<line>\d+)│(?P<message>[\s\S]*)')
class ElmLintBear:
    """
    This bear formats the Elm source code according to a standard set of rules.

    See <https://github.com/avh4/elm-format> for more information.
    """

    LANGUAGES = {'Elm'}
    REQUIREMENTS = {NpmRequirement('elm', '0.18')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting'}

    @classmethod
    def check_prerequisites(cls):
        if which('elm-format') is None:
            return ('elm-format is missing. Download it from '
                    'https://github.com/avh4/elm-format/blob/master/README.md'
                    '#for-elm-018 and put it into your PATH.')
        else:
            return True

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename, '--yes'
