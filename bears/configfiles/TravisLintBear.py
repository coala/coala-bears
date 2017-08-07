from coalib.bearlib.abstractions.Linter import linter

from dependency_management.requirements.GemRequirement import GemRequirement


@linter(executable='travis',
        output_format='regex',
        output_regex=r'\[x\]\s+(?P<message>.+)')
class TravisLintBear:
    """
    A validator for your ``.travis.yml`` that attempts to reduce common build
    errors such as:

    - invalid YAML
    - missing language key
    - unsupported runtime versions of Ruby, PHP, OTP, etc.
    - deprecated features or runtime aliases
    """

    LANGUAGES = {'YAML'}
    REQUIREMENTS = {GemRequirement('travis', '1.8.8')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax'}
    SEE_MORE = 'https://docs.travis-ci.com/user/travis-lint'

    @staticmethod
    def create_arguments(filename, file, config_file):
        return 'lint', filename
