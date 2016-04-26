from coalib.bearlib.abstractions.Linter import linter


@linter(executable='mcs',
        use_stdout=False,
        use_stderr=True,
        output_format='regex',
        output_regex=r'.+\((?P<line>\d+),(?P<column>\d+)\): '
                     r'(?P<severity>error|warning) \w+: (?P<message>.+)')
class CSharpLintBear:
    """
    Checks C# code for syntactical correctness using the ``mcs`` compiler.
    """

    LANGUAGES = "C#"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
