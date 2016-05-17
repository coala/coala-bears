from coalib.bearlib.abstractions.Linter import linter


@linter(executable='goimports',
        use_stdin=True,
        output_format='corrected',
        result_message='Imports need to be added/removed.')
class GoImportsBear:
    """
    Adds/Removes imports to Go code for missing imports.
    """
    LANGUAGES = "Go"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ()
