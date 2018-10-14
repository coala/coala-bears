from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.LuarocksRequirement import (
    LuarocksRequirement)


@linter(executable='luacheck',
        use_stdin=True,
        output_format='regex',
        output_regex=r'stdin:(?P<line>\d+):(?P<column>\d+)-'
                     r'(?P<end_column>\d+): '
                     r'\((?P<severity>[WE])(?P<origin>\d+)\) (?P<message>.+)')
class LuaLintBear:
    """
    Check Lua code for possible semantic problems, like unused code.

    Read more at <https://github.com/mpeterv/luacheck>.
    """

    LANGUAGES = {'Lua'}
    REQUIREMENTS = {LuarocksRequirement('luacheck')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Unreachable Code', 'Unused Code', 'Variable Misuse'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '-', '--formatter=plain', '--ranges', '--codes'
