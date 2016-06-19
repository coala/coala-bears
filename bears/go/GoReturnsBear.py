from coalib.bearlib.abstractions.Linter import linter


@linter(executable='goreturns',
        use_stdin=True,
        output_format='corrected',
        result_message='Imports or returns need to be added/removed.')
class GoReturnsBear:
    """
    Proposes corrections of Go code using ``goreturns``.
    """
    LANGUAGES = {"Go"}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Security'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ()
