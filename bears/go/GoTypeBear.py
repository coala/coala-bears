from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.GoRequirement import GoRequirement


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
    REQUIREMENTS = {GoRequirement(
        package='golang.org/x/tools/cmd/gotype', flag='-u')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/40055'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '-e', filename
