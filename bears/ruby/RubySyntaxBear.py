from coalib.bearlib.abstractions.Linter import linter


@linter(executable='ruby',
        use_stdout=False,
        use_stderr=True,
        output_format='regex',
        output_regex=r'.+?:(?P<line>\d+): (?P<message>.*?'
                     r'(?P<severity>error|warning)[,:] \S+)\s?'
                     r'(?:\S+\s(?P<column>.*?)\^)?')
class RubySyntaxBear:
    """
    Checks the code with ``ruby -wc`` on each file separately.
    """
    LANGUAGES = "Ruby"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '-wc', filename
