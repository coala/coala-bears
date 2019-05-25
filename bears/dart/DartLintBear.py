from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


@linter(executable='dartanalyzer',
        output_format='regex',
        output_regex=r'\[(?P<severity>error|warning)\] (?P<message>.+)\('
                     r'.+, line (?P<line>\d+), col (?P<column>\d+)\)')
class DartLintBear:
    """
    Checks the code with ``dart-linter``.

    This bear expects dart commands to be on your ``PATH``. Please ensure
    /path/to/dart-sdk/bin is in your ``PATH``.
    """
    LANGUAGES = {'Dart'}
    REQUIREMENTS = {DistributionRequirement(brew='dart')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         use_spaces: bool = True,
                         indent_size: int = 2,
                         ):
        # use_spaces must be True and indent_size must be 2 because
        # dartanalyzer only supports these settings
        # see https://github.com/dart-lang/dart_style/issues/261
        if (indent_size != 2 or not use_spaces):
            raise ValueError(
                'DartLintBear only supports `use_spaces=True` '
                'and `indent_size=2`'
            )
        return filename,
