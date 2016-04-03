from coalib.bearlib.abstractions.Linter import linter


@linter(executable='go',
        use_stdout=False,
        use_stderr=True,
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+): (?P<message>.*)')
class GoVetBear:
    """
    Checks the code using ``go vet``.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return 'vet', filename
