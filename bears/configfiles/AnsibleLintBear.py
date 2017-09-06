from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement


@linter(executable='ansible-lint',
        output_format='regex',
        output_regex=r'')
class AnsibleLintBear:
    '''
    Check and correct ansible playbooks using ``ansible-lint``.

    See <https://github.com/willthames/ansible-lint/> for details about the tool.
    '''

    LANGUAGES = {'Ansible'}
    REQUIREMENTS = {PipRequirement('ansible-lint', '3.4.12')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = ''
    CAN_FIX = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file):
        return
