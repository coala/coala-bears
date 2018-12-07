from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GemRequirement import GemRequirement


@linter(executable='slim-lint',
        output_format='regex',
        output_regex=r'(?P<origin>/[a-zA-Z].+):(?P<line>\d+)'
                     r'\s\[(?P<severity>[a-zA-Z]+)\]\s(?P<message>.*)$')
class SlimLintBear:  # pragma nt: no cover
    """
    Linter for slim language.
    SEE_MORE = 'https://github.com/sds/slim-lint'
    """
    LANGUAGES = {'Slim'}
    REQUIREMENTS = {GemRequirement('slim_lint', '0.16.1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         slimlint_config: str = ''):
        """
        :param slimlint_config: Path to a custom configuration file.
        """
        if slimlint_config:
            return ('--reporter=default --config=' + slimlint_config, filename)
        else:
            return ('--reporter=default', filename)
