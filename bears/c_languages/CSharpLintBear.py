from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.DistributionRequirement import (
    DistributionRequirement)


@linter(executable='mcs',
        use_stdout=False,
        use_stderr=True,
        output_format='regex',
        output_regex=r'.+\((?P<line>\d+),(?P<column>\d+)\): '
                     r'(?P<severity>error|warning) \w+: (?P<message>.+)')
class CSharpLintBear:
    """
    Checks C# code for syntactical correctness using the ``mcs`` compiler.
    """

    LANGUAGES = {"C#"}
    REQUIREMENTS = {DistributionRequirement(apt_get='mono-mcs')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
