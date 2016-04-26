from coalib.bearlib.abstractions.Linter import linter


@linter(executable='sqlint', use_stdin=True, output_format="regex",
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+):'
                     r'(?P<severity>ERROR|WARNING) (?P<message>(?:\s*.+)*)')
class SQLintBear:
    """
    Check the given SQL files for syntax errors or warnings.

    This bear supports ANSI syntax. Check out
    <https://github.com/purcell/sqlint> for more detailed information.
    """

    LANGUAGES = "SQL"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ()
