from coalib.bearlib.abstractions.Linter import linter


@linter(executable='postcss',
        output_format='corrected',
        result_message='Add vendor prefixes to CSS rules.',
        prerequisite_check_command=('postcss', '--use', 'autoprefixer'),
        prerequisite_check_fail_message='Autoprefixer is not installed.')
class CSSAutoPrefixBear:
    """
    This bear adds vendor prefixes to CSS rules using ``autoprefixer`` utility.
    """
    LANGUAGES = "CSS"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--use', 'autoprefixer', filename
