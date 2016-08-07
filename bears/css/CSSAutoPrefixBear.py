from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.NpmRequirement import NpmRequirement


@linter(executable='postcss',
        output_format='corrected',
        result_message='Add vendor prefixes to CSS rules.',
        prerequisite_check_command=('postcss', '--use', 'autoprefixer'),
        prerequisite_check_fail_message='Autoprefixer is not installed.')
class CSSAutoPrefixBear:
    """
    This bear adds vendor prefixes to CSS rules using ``autoprefixer`` utility.
    """
    LANGUAGES = {"CSS"}
    REQUIREMENTS = {NpmRequirement('postcss-cli', '2'),
                    NpmRequirement('autoprefixer', '6')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/40093'
    CAN_FIX = {'Syntax', 'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--use', 'autoprefixer', filename
