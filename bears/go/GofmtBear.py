from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GoRequirement import GoRequirement


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
    LANGUAGES = {'Go'}
    REQUIREMENTS = {GoRequirement(package='golang.org/cmd/gofmt', flag='-u')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}
    ASCIINEMA_URL = 'https://asciinema.org/a/94812'

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ()
