from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(executable='happiness',
        output_format='regex',
        output_regex=r'\s.+:(?P<line>\d+):(?P<column>\d+):(?P<message>.+)')
class HappinessLintBear:
    """
    Checks JavaScript files for semantic and syntax errors using ``happiness``.

    See <https://github.com/JedWatson/happiness/> for more information.
    """
    LANGUAGES = {'JavaScript'}
    REQUIREMENTS = {NpmRequirement('happiness', '7.1.2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/80714'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(
            filename, file, config_file,
            use_spaces: bool=False):

        # Refer to https://github.com/coala/coala-bears/issues/1754
        # use_spaces = true conflicts with HappinessLintBear as
        # it requires tab indentations.
        if (use_spaces):
            raise ValueError(
                'Please set `use_spaces=False` with HappinessLintBear'
                'to avoid conflicts with other Bears'
            )
        return filename,
