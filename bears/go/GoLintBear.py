import shlex

from coalib.bearlib.abstractions.Linter import linter


@linter(executable='golint',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+): (?P<message>.*)')
class GoLintBear:
    """
    Checks the code using ``golint``. This will run golint over each file
    separately.
    """
    LANGUAGES = "Go"

    @staticmethod
    def create_arguments(filename, file, config_file,
                         golint_cli_options: str=''):
        """
        :param golint_cli_options: Any other flags you wish to pass to golint.
        """
        args = ()
        if golint_cli_options:
            args += tuple(shlex.split(golint_cli_options))
        return args + (filename,)
