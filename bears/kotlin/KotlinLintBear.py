from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


@linter(executable='ktlint',
        global_bear=True,
        output_format='regex',
        output_regex=r'(?P<line>\d+):(?P<column>\d+): '
                     r'(?P<message>.+)')
class KotlinLintBear:
    """
    Lints your Kotlin files.
    Checks for coding standards or semantic problems in Kotlin files.
    """
    LANGUAGES = {'kotlin'}
    REQUIREMENTS = {DistributionRequirement(brew='shyiko/ktlint/ktlint')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax'}
    SEE_MORE = 'https://ktlint.github.io'

    @staticmethod
    def create_arguments(config_file):
        return ()
