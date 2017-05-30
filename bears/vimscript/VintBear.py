from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PackageRequirement import (
    PackageRequirement)


@linter(executable='vint', output_format='regex',
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+): (?P<message>.+)')
class VintBear:
    """
    Check vimscript code for possible style problems.

    See <https://github.com/Kuniwak/vint> for more information.
    """

    LANGUAGES = {'VimScript'}
    REQUIREMENTS = {PackageRequirement('broken', 'vim-vint', '0.3.10')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
