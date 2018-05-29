import shlex

from coalib.bearlib.abstractions.Linter import linter


@linter(executable='oclint',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+): (?P<message>.*)')
class OClintBear:
    """
    OCLint is a static code analysis tool for improving quality and
    reducing defects by inspecting C, C++ and Objective-C code.

    For more information, consult <http://oclint.org/>.
    """

    LANGUAGES = {'C', 'C++', 'Objective-C'}
    CAN_DETECT = {'Formatting', 'Duplication', 'Syntax', 'Complexity', 'Smell',
                  'Redundancy', 'Unreachable Code'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    @staticmethod
    def create_arguments(filename, file, config_file,
                         oclint_cli_options: str=''):
        """
        :param oclint_cli_options: Any other flags you wish to pass to oclint.
        """
        args = ()
        if oclint_cli_options:
            args += tuple(shlex.split(oclint_cli_options))
        return args + (filename,)
