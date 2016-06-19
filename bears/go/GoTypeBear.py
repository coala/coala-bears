from coalib.bearlib.abstractions.Linter import linter


@linter(executable='gotype',
        use_stdout=False,
        use_stderr=True,
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+): *(?P<message>.*)')
class GoTypeBear:
    """
    Checks the code using ``gotype``. This will run ``gotype`` over each file
    separately.
    """
    LANGUAGES = {"Go"}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '-e', filename
