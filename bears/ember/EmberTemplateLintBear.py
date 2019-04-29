import os

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(executable='ember-template-lint',
        output_format='regex',
        output_regex=r'(?P<line>\d+):(?P<column>\d+)(?P<message>.*)'
        )
class EmberTemplateLintBear:
    """
    ember-template-lint lints templates and return error results.

    This is commonly used through ember-cli-template-lint which
    adds failing lint tests for consuming ember-cli applications.

    https://github.com/ember-template-lint/ember-template-lint
    """

    LANGUAGES = {'Ember'}
    REQUIREMENTS = {NpmRequirement('ember-template-lint', '1.1.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}
    SEE_MORE = 'https://github.com/ember-template-lint/ember-template-lint'

    @staticmethod
    def create_arguments(filename, file, config_file,
                         custom_config: str = os.devnull):
        """
        :param custom_config:
            The configuration file Ember-Template-Lint shall use.
        """
        return ('--config-path',
                custom_config if custom_config else config_file,
                filename)
