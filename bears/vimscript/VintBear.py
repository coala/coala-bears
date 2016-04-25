from coalib.bearlib.abstractions.Linter import linter


@linter(executable='vint',
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+): (?P<message>.+)')
class VintBear:
    """
    Check vimscript code for possible style problems.

    See <https://github.com/Kuniwak/vint> for more information.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
