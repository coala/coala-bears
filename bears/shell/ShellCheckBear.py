from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)
from dependency_management.requirements.AnyOneOfRequirements import (
    AnyOneOfRequirements)
from dependency_management.requirements.CabalRequirement import (
     CabalRequirement)


@linter(executable='shellcheck', output_format='regex',
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+): '
                     r'(?P<severity>error|warning|info): (?P<message>.+)')
class ShellCheckBear:
    """
    Check bash/shell scripts for syntactical problems (with understandable
    messages), semantical problems as well as subtle caveats and pitfalls.

    A gallery of bad code that can be detected is available at
    <https://github.com/koalaman/shellcheck/blob/master/README.md>.
    """

    LANGUAGES = {'sh', 'bash', 'ksh', 'dash'}
    REQUIREMENTS = {AnyOneOfRequirements(
            [CabalRequirement('ShellCheck', '0.4.1'),
             DistributionRequirement('shellcheck')
             ]
        ),
    }
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Security', 'Undefined Element', 'Unused Code'}

    @staticmethod
    def create_arguments(filename, file, config_file, shell: str = 'sh',
                         shellcheck_ignore: list = None,
                         ):
        """
        :param shell: Target shell being used.
        :param shellcheck_ignore: List of linting rules that should be ignored.
        """
        args = ('--f', 'gcc', '-s', shell, filename)
        if shellcheck_ignore:
            args += ('-e', ','.join(shellcheck_ignore))

        return args
