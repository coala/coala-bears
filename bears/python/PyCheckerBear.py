import shlex

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.DistributionRequirement import (
        DistributionRequirement)


@linter(executable='pychecker',
        output_format='regex',
        output_regex=r'(?P<filename>\w+\.py):(?P<line>\d+): '
                     r'(?P<message>.*)')
class PyCheckerBear:
    """
    Find bugs in your Python source code.
    The code for each function, class, and method is checked for possible
    problems. Checks for unused globals and locals(module or variable), unused
    method arguments and using a variable before setting it or if you are
    redefining a function/class/method in the same scope.
    """
    LANGUAGES = {'Python', 'Python 2', 'Python 3'}
    REQUIREMENTS = {DistributionRequirement(apt_get='pychecker')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Unused method/function arguments',
                  'No doc string', 'Redefining'}
    SEE_MORE = 'http://pychecker.sourceforge.net/'

    @staticmethod
    def create_arguments(filename, file, config_file,
                         pychecker_cli_options: str = ''):
        """
        :param pychecker_cli_options: Command line options you wish to be
                                      passed to pychecker.
        """
        args = ()
        if pychecker_cli_options:
            args += tuple(shlex.split(pychecker_cli_options))

        return args + (filename,)
