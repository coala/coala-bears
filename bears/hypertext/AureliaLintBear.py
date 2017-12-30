from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement



@linter(executable='template-lint',
        output_format='regex',
        output_regex=r'L(?P<line>\d+)C(?P<column>\d+): (?P<message>.*)')
class AureliaLintBear:
    """
    Check code for syntactical or semantical errors.
    """
    LANGUAGES = {'HTML'}
    REQUIREMENTS = {NpmRequirement('template-lint')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--format=compact', filename
