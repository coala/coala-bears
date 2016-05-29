from coalib.bearlib.abstractions.Linter import linter


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

    LANGUAGES = "Lua"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return "-", "--formatter=plain", "--ranges", "--codes"
