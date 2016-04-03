from coalib.bearlib.abstractions.Linter import linter


@linter(executable='cppclean',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+):(?P<message>.*)')
class CPPCleanBear:
    """
    Checks code with ``cppclean``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
