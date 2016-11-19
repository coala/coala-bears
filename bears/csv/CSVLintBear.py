from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.GemRequirement import GemRequirement


@linter(executable='csvlint',
        output_format='regex',
        output_regex=r'\d\. (?P<message>.+(s|g|e|w|d)\.*)'
                     r'( |$)(?P<additional_info>.*)')
class CSVLintBear:
    """
    Verifies using ``csvlint`` if ``.csv`` files are valid CSV or not.
    """

    LANGUAGES = {'CSV'}
    REQUIREMENTS = {GemRequirement('csvlint')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
