from coalib.bearlib.abstractions.Linter import linter


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
    LANGUAGES = "CSS"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--format=compact', filename
