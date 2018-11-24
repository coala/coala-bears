import subprocess
import sys

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(executable='alex',
        output_format='regex',
        output_regex=r'(?P<line>\d+):(?P<column>\d+)-(?P<end_line>\d+):'
                     r'(?P<end_column>\d+)\s+(?P<severity>warning)\s+'
                     r'(?P<message>.+)')
class AlexBear:
    """
    Checks the markdown file with Alex - Catch insensitive, inconsiderate
    writing.

    Be aware that Alex and this bear only work on English text.
    For more information, consult <https://www.npmjs.com/package/alex>.
    """
    LANGUAGES = {'Natural Language'}
    REQUIREMENTS = {NpmRequirement('alex', '3')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    @classmethod
    def check_prerequisites(cls):
        parent_prereqs = super().check_prerequisites()
        if parent_prereqs is not True:
            return parent_prereqs

        incorrect_pkg_msg = (
            'Please ensure that the package that has been installed is the '
            "one to 'Catch insensitive, inconsiderate writing'. This can be "
            'verified by running `alex --help` and seeing what it does.')
        try:
            output = subprocess.check_output(('alex', '--help'),
                                             stderr=subprocess.STDOUT)
        except (OSError, subprocess.CalledProcessError):
            return ('The `alex` package could not be verified. ' +
                    incorrect_pkg_msg)
        else:
            output = output.decode(sys.getfilesystemencoding())
            if 'Catch insensitive, inconsiderate writing' in output:
                return True
            else:
                return ("The `alex` package that's been installed seems to "
                        'be incorrect. ' + incorrect_pkg_msg)

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
