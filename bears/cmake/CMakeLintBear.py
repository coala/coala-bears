from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.PipRequirement import PipRequirement
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
    REQUIREMENTS = {PipRequirement('cmakelint', '1.*')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         cmakelint_config: path=""):
        """
        :param cmakelint_config: The location of the cmakelintrc config file.
        """
        args = ()
        if cmakelint_config:
            args += ('--config=' + cmakelint_config,)
        return args + (filename,)
