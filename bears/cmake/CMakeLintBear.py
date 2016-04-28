from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import path


@linter(executable='cmakelint',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+): (?P<message>.*)')
class CMakeLintBear:
    """
    Checks the code with ``cmakelint``.
    """
    LANGUAGES = 'CMake'

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
