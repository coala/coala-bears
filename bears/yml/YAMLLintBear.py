from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.PipRequirement import PipRequirement


@linter(executable='yamllint',
        output_format="regex",
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+): '
                     r'\[(?P<severity>error|warning)\] (?P<message>.+)')
class YAMLLintBear:
    """
    Check yaml code for errors and possible problems.

    You can read more about capabilities at
    <http://yamllint.readthedocs.org/en/latest/rules.html>.
    """

    LANGUAGES = {"YAML"}
    REQUIREMENTS = {PipRequirement('yamllint', '1.*')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file, yamllint_config: str=''):
        """
        :param yamllint_config: Path to a custom configuration file.
        """
        args = ('-f', 'parsable', filename)
        if yamllint_config:
            args += ('--config=' + yamllint_config,)
        return args
