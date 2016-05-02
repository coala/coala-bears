from coalib.bearlib.abstractions.Linter import linter


@linter(executable='chktex',
        output_format='regex',
        output_regex=r'(?P<severity>Error|Warning) \d+ in .+ line '
                     r'(?P<line>\d+): (?P<message>.*)')
class LatexLintBear:
    """
    Checks the code with ``chktex``.
    """
    LANGUAGES = "Tex"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
