from coalib.bearlib.abstractions.Linter import linter


@linter(executable='gofmt',
        use_stdin=True,
        output_format='corrected',
        result_message='Formatting can be improved.')
class GofmtBear:
    """
    Suggest better formatting options in Go code. Basic checks like alignment,
    indentation, and redundant parentheses are provided.

    This is done using the ``gofmt`` utility. For more information visit
    <https://golang.org/cmd/gofmt/>.
    """
    LANGUAGES = "Go"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ()
