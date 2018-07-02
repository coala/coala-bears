from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GemRequirement import GemRequirement


@linter(executable='sqlint', use_stdin=True, output_format='regex',
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+):'
                     r'(?P<severity>ERROR|WARNING) (?P<message>(?:\s*.+)*)')
class SQLintBear:
    """
    Check the given SQL files for syntax errors or warnings.

    This bear supports ANSI syntax. Check out
    <https://github.com/purcell/sqlint> for more detailed information.
    """

    LANGUAGES = {'SQL'}
    REQUIREMENTS = {GemRequirement('sqlint', '0.1.5')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ()
