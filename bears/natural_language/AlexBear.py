from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.NpmRequirement import NpmRequirement


@linter(executable='alex',
        output_format='regex',
        output_regex=r'(?P<line>\d+):(?P<column>\d+)-(?P<end_line>\d+):'
                     r'(?P<end_column>\d+)\s+(?P<severity>warning)\s+'
                     r'(?P<message>.+)')
class AlexBear:
    """
    Checks the markdown file with Alex - Catch insensitive, inconsiderate
    writing.
    """
    LANGUAGES = {"Natural Language"}
    REQUIREMENTS = {NpmRequirement('alex', '2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
