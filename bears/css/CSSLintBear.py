from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(executable='csslint',
        output_format='regex',
        output_regex=r'.+: *(?:line (?P<line>\d+), '
                     r'col (?P<column>\d+), )?(?P<severity>Error|Warning) - '
                     r'(?P<message>.*)')
class CSSLintBear:
    """
    Check code for syntactical or semantical problems that might lead to
    problems or inefficiencies.
    """
    LANGUAGES = {'CSS'}
    REQUIREMENTS = {NpmRequirement('csslint', '1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Code Simplification'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--format=compact', filename
