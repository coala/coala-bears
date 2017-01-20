from shutil import which

from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.NpmRequirement import NpmRequirement


@linter(executable='elm-format',
        output_format='corrected')
class ElmLintBear:
    """
    This bear checks the formatting of the Elm code.

    See <https://github.com/avh4/elm-format> for more information.
    """

    LANGUAGES = {'Elm'}
    REQUIREMENTS = {NpmRequirement('elm', '0.18')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting'}

    @classmethod
    def check_prerequisites(cls):
        if which('elm-format') is None:
            return ('elm-format is missing. Download it from'
                    '<https://github.com/avh4/elm-format/blob/master/README.md#for-elm-018>'
                    'and put it in your PATH.')
        else:
            return True

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--stdin', filename
