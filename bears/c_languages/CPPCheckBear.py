from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.DistributionRequirement import (
    DistributionRequirement)
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Setting import typed_list


@linter(executable='cppcheck',
        use_stdout=False,
        use_stderr=True,
        output_format='regex',
        output_regex=r'(?P<line>\d+):(?P<severity>[a-zA-Z]+):'
                     r'(?P<origin>[a-zA-Z]+):(?P<message>.*)',
        severity_map={'error': RESULT_SEVERITY.MAJOR,
                      'warning': RESULT_SEVERITY.NORMAL,
                      'style': RESULT_SEVERITY.INFO})
class CPPCheckBear:
    """
    Report possible security weaknesses for C/C++.
    For more information, consult <https://github.com/danmar/cppcheck>.
    """

    LANGUAGES = {'C', 'C++'}
    REQUIREMENTS = {DistributionRequirement(apt_get='cppcheck')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Security', 'Unused Code', 'Unreachable Code', 'Smell'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         enable: typed_list(str)=[]):
        """
        :param enable:
            Choose specific issues to report. Issues that can be
            reported are: all, warning, style, performance,
            portability, information, unusedFunction,
            missingInclude
        """
        args = ('--template={line}:{severity}:{id}:{message}',)

        if enable:
            args += ('--enable=' + ','.join(enable),)

        return args + (filename,)
