from coalib.bearlib.abstractions.Linter import linter


@linter(executable='infer',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+): (?P<severity>error|warning): '
                     r'(?P<message>.*)')
class InferBear:
    """
    Checks the code with ``infer``.
    """
    LANGUAGES = "Java"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '-nbp', '--', 'javac', filename
