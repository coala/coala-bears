from coalib.bearlib.abstractions.Linter import linter


@linter(executable='yamllint',
        output_format="regex",
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+): '
                     r'\[(?P<severity>error|warning)\] (?P<message>.+)')
class YAMLLintBear:
    """
    Checks the code with ``yamllint`` on each file separately.
    """

    @staticmethod
    def create_arguments(filename, file, config_file, yamllint_config: str=''):
        """
        :param yamllint_config: Path to a custom configuration file.
        """
        args = ('-f', 'parsable', filename)
        if yamllint_config:
            args += ('--config=' + yamllint_config,)
        return args
