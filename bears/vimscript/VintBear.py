from coalib.bearlib.abstractions.Linter import linter


@linter(executable='vint',
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+): (?P<message>.+)')
class VintBear:
    """
    Checks vimscript code for possible problems using ``vint-linter``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
