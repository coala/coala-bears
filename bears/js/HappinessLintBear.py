from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.NpmRequirement import NpmRequirement


@linter(executable='happiness',
        output_format='regex',
        output_regex=r'\s*.+:(?P<line>\d+):(?P<column>\d+):(?P<message>.+)'
        )
class HappinessLintBear:
    """
    Checks the js files using ``happiness`` for semantic and syntax errors.

    See <https://github.com/JedWatson/happiness/> for more information.
    """
    LANGUAGES = {"JavaScript"}
    REQUIREMENTS = {NpmRequirement('happiness', '7.1.2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
