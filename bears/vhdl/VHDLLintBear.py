from shutil import which

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


@linter(executable='perl',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+):(?P<severity>.*) - (?P<message>.*)')
class VHDLLintBear:
    """
    Check VHDL code for common codestyle problems.

    Rules include:

     * Signals, variables, ports, types, subtypes, etc. must be lowercase.
     * Constants and generics must be uppercase.
     * Entities, architectures and packages must be "mixedcase" (may be 100%
       uppercase, but not 100% lowercase).
     * Ports must be suffixed using _i, _o or _io denoting its kind.
     * Labels must be placed in a separated line. Exception: component
       instantiation.
     * End statements must be documented indicating what are finishing.
     * Buffer ports are forbidden.
     * VHDL constructions of the "entity xxxx is" and similars must be in one
       line. You can't put "entity xxxxx" in one line and "is" in another.
     * No more than one VHDL construction is allowed in one line of code.

    See <http://fpgalibre.sourceforge.net/ingles.html#tp46> for more
    information.
    """

    LANGUAGES = {'VHDL'}
    REQUIREMENTS = {DistributionRequirement('perl')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting'}

    @classmethod
    def check_prerequisites(cls):
        if which('perl') is None:
            return 'perl is not installed.'
        elif which('bakalint.pl') is None:
            return ('bakalint is missing. Download it from '
                    '<http://fpgalibre.sourceforge.net/ingles.html#tp46> and '
                    'put it into your PATH.')
        else:
            return True

    @staticmethod
    def create_arguments(filename, file, config_file):
        return which('bakalint.pl'), '--input', filename
