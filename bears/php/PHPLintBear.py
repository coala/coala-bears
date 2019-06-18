from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


@linter(executable='php',
        use_stderr=True,
        output_format='regex',
        output_regex=r'(?P<severity>Parse|Fatal) error: (?P<message>.*)'
                     r'(?: in .* on line (?P<line>\d+))?',
        severity_map={'Parse': RESULT_SEVERITY.MAJOR,
                      'Fatal': RESULT_SEVERITY.MAJOR})
class PHPLintBear:
    """
    Checks the code with ``php -l``. This runs it on each file separately.
    """
    LANGUAGES = {'PHP'}
    REQUIREMENTS = {DistributionRequirement(apt_get='php-cli')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ('-l', '-n', '-d', 'display_errors=On', '-d', 'log_errors=Off',
                filename)
