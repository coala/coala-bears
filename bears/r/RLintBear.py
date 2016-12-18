from coala_utils.string_processing import escape

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.RscriptRequirement import (
    RscriptRequirement)
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='Rscript',
        output_format='regex',
        output_regex=r'.*?:(?P<line>\d+):(?P<column>\d+): '
                     r'(?P<severity>\S+): (?P<message>.*)',
        severity_map={'style': RESULT_SEVERITY.NORMAL,
                      'warning': RESULT_SEVERITY.NORMAL,
                      'error': RESULT_SEVERITY.MAJOR},
        prerequisite_check_command=('Rscript', '-e', 'library(lintr)'),
        prerequisite_check_fail_message='R library "lintr" is not installed.')
class RLintBear:
    """
    Checks the code with ``lintr``.
    """
    LANGUAGES = {'R'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    REQUIREMENTS = {RscriptRequirement(package='lintr', flag='-e',
                                       repo='http://cran.rstudio.com')}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ('-e', 'library(lintr)', '-e',
                'lintr::lint("' + escape(filename, '\\"') + '")')
