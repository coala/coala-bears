from coalib.bearlib.abstractions.Linter import linter


@linter(executable='goreturns',
        use_stdin=True,
        output_format='corrected',
        result_message='Imports or returns need to be added/removed.')
class GoReturnsBear:
    """
    Proposes corrections of Go code using ``goreturns``.
    """
    LANGUAGES = "Go"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ()
