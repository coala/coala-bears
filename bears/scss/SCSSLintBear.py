from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.GemRequirement import GemRequirement


@linter(executable='scss-lint', output_format="regex",
        output_regex=r'.+:(?P<line>\d+)\s+(\[(?P<severity>.)\])\s*'
                     r'(?P<message>.*)')
class SCSSLintBear:
    """
    Check SCSS code to keep it clean and readable.

    More information is available at <https://github.com/brigade/scss-lint>.
    """

    LANGUAGES = {"SCSS"}
    REQUIREMENTS = {GemRequirement('scss-lint', '', 'false')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
