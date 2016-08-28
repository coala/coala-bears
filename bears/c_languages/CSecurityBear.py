from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.DistributionRequirement import (
    DistributionRequirement)
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
    REQUIREMENTS = {DistributionRequirement(apt_get='flawfinder')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/7z8ol9mpsgtuo1096c6jk8hi6'
    CAN_DETECT = {'Security', 'Memory Leak', 'Code Simplification'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return "--columns", "--dataonly", "--quiet", "--singleline", filename
