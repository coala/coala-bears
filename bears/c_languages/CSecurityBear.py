from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable="flawfinder",
        output_format="regex",
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+):\s*'
                     r'\[(?P<severity>\d)\]\s*'
                     r'\((?P<origin>.+)\) (?P<message>.+)',
        severity_map={"1": RESULT_SEVERITY.INFO,
                      "2": RESULT_SEVERITY.INFO,
                      "3": RESULT_SEVERITY.NORMAL,
                      "4": RESULT_SEVERITY.NORMAL,
                      "5": RESULT_SEVERITY.MAJOR},
        prerequisite_check_command=('flawfinder',),
        prerequisite_check_fail_message=('Flawfinder needs to be run with '
                                         'python2.'))
class CSecurityBear:
    """
    Report possible security weaknesses for C/C++.

    For more information, consult <http://www.dwheeler.com/flawfinder/>.
    """

    LANGUAGES = {'C', 'C++'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Security', 'Memory Leak', 'Code Simplification'}

    @staticmethod
    def create_arguments(filename, file, config_file, neverignore: bool=False):
        """
        :param neverignore:
            Never ignore security issues, even if they have an ``ignore''
            directive in a comment.
        """
        args = "--columns", "--dataonly", "--quiet", "--singleline"
        args += ("--neverignore", filename) if neverignore else (filename,)
        return args
