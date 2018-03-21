import shlex

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.ExecutableRequirement import (
    ExecutableRequirement)


@linter(executable='mlint',
        use_stderr=True,
        output_format='regex',
        output_regex=r'L (?P<line>\d+) \(C (?P<column>\d+)'
                     r'(?:-(?P<end_column>\d+))*\): (?P<message>.*)')
class MlintBear:
    """
    Checks the code with mlint. This will run mlint over each file
    separately.
    """
    LANGUAGES = {'Matlab'}
    REQUIREMENTS = {ExecutableRequirement('mlint')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Unused Code', 'Formatting', 'Duplication',
                  'Syntax'}
    SEE_MORE = 'https://www.mathworks.com/help/matlab/ref/mlint.html'

    @staticmethod
    def create_arguments(filename, file, config_file,
                         mlint_cli_options: str=''):
        """
        :param mlint_cli_options: Any other flags you wish to be
                                  passed to mlint.
        """
        args = ()
        if mlint_cli_options:
            args += tuple(shlex.split(mlint_cli_options))

        return args + (filename,)
