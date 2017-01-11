from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.CabalRequirement import (
    CabalRequirement)


@linter(executable='ghc-mod',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+):'
                     r'(?P<message>.+)')
class GhcModBear:
    """
    Syntax checking with ``ghc`` for Haskell files.

    See <https://hackage.haskell.org/package/ghc-mod> for more information!
    """

    LANGUAGES = {'Haskell'}
    REQUIREMENTS = {CabalRequirement(package='ghc-mod', version='5.6.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/98873'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        # -b '. ' is the argument given for ghc-mod for seperation of messages
        return '-b', '. ', 'check', filename
