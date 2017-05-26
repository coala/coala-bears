from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement


@linter(executable='cppclean',
        executable_check_fail_info='Please see https://github.com/myint/cppclean#installation '
                                   'for more information about this.',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+):(?P<message>.*)')
class CPPCleanBear:
    """
    Find problems in C++ source code that slow down development in large code
    bases. This includes finding unused code, among other features.

    Read more about available routines at
    <https://github.com/myint/cppclean#features>.
    """

    LANGUAGES = {'C++'}
    REQUIREMENTS = {PipRequirement('cppclean', '0.12.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Smell', 'Unused Code', 'Security'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
