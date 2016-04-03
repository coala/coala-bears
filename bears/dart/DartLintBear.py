from coalib.bearlib.abstractions.Linter import linter


@linter(executable='dartanalyzer',
        output_format='regex',
        output_regex=r'\[(?P<severity>error|warning)\] (?P<message>.+)\('
                     r'.+, line (?P<line>\d+), col (?P<column>\d+)\)')
class DartLintBear:
    """
    Checks the code with ``dart-linter``.

    This bear expects dart commands to be on your ``PATH``. Please ensure
    /path/to/dart-sdk/bin is in your ``PATH``.
    """
    LANGUAGES = "Dart"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
