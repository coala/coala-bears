import sys

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.settings.Setting import path


@linter(executable='cmakelint',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+): (?P<message>.*)')
class CMakeLintBear:
    """
    Check CMake code for syntactical or formatting issues.

    For more information consult <https://github.com/richq/cmake-lint>.
    """
    LANGUAGES = {'CMake'}
    REQUIREMENTS = {PipRequirement('cmakelint', '1.3')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         max_line_length: int=80,
                         cmakelint_config: path=''):
        """
        :param max_line_length:
             Maximum number of characters for a line.
             When set to 0 allows infinite line length.
        :param cmakelint_config: The location of the cmakelintrc config file.
        """
        if not max_line_length:
            max_line_length = sys.maxsize

        args = ()
        if cmakelint_config:
            args += ('--config=' + cmakelint_config,)

        args += ('--linelength=' + str(max_line_length),)

        return args + (filename,)
