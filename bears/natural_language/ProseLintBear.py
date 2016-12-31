from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement


@linter(executable='proselint',
        output_format='regex',
        output_regex=r'.+?:(?P<line>\d+):(?P<column>\d+): \S* (?P<message>.+)')
class ProseLintBear:
    """
    Lints the file using `proselint <https://github.com/amperser/proselint>`__.
    Works only with English language text.
    """
    LANGUAGES = {'Natural Language'}
    REQUIREMENTS = {PipRequirement('proselint', '0.7.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Spelling', 'Syntax', 'Formatting', 'Grammar'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
