from coalib.bearlib.abstractions.Linter import linter


@linter(executable='phan',
        output_format='regex',
        output_regex=r'(?P<filename>.+):(?P<line>\d+)\s(?P<message>.+)')
class PhanBear:
    """
    Phan is a static analyzer for PHP that looks for common issues and will
    verify type compatibility on various operations when type information is
    available or can be deduced.

    See <https://github.com/etsy/phan> for more information.
    """
    LANGUAGES = {'PHP'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax', 'Documentation',
                  'Code Simplification'}
    ASCIINEMA_URL = ''

    def create_argument(file, filename, config_file):
        return (filename,)
