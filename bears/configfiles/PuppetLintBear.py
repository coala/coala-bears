from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GemRequirement import GemRequirement


@linter(executable='puppet-lint',
        output_format='regex',
        output_regex=r'(?P<line>\d+):(?P<column>\d+):'
                     r'(?P<severity>warning|error):(?P<message>.+)')
class PuppetLintBear:
    '''
    Check and correct puppet configuration files using ``puppet-lint``.

    See <http://puppet-lint.com/> for details about the tool.
    '''

    LANGUAGES = {'Puppet'}
    REQUIREMENTS = {GemRequirement('puppet-lint', '2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/87751'
    CAN_FIX = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ('--log-format', '%{line}:%{column}:%{kind}:%{message}',
                filename)
