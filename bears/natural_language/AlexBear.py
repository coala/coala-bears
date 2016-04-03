from coalib.bearlib.abstractions.Linter import linter


@linter(executable='alex',
        output_format='regex',
        output_regex=r'(?P<line>\d+):(?P<column>\d+)-(?P<end_line>\d+):'
                     r'(?P<end_column>\d+) (?P<severity>warning) '
                     r'(?P<message>.+)')
class AlexBear:
    """
    Checks the markdown file with Alex - Catch insensitive, inconsiderate
    writing.
    """
    LANGUAGES = "Natural Language"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
