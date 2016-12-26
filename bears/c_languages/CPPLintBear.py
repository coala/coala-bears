from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.settings.Setting import typed_list


def check_invalid_config(use_spaces, indent_size):
    if not use_spaces or indent_size != 2:
        raise ValueError("CPPLint doesn't support indent_size other "
                         'than 2 or not using spaces.')


@linter(executable='cpplint',
        use_stdout=False,
        use_stderr=True,
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+): (?P<message>.+)')
class CPPLintBear:
    """
    Check C++ code for Google's C++ style guide.

    For more information, consult <https://github.com/theandrewdavis/cpplint>.
    """

    LANGUAGES = {'C++'}
    REQUIREMENTS = {PipRequirement('cpplint', '1.3')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         max_line_length: int=79,
                         cpplint_ignore: typed_list(str)=(),
                         cpplint_include: typed_list(str) = (),
                         indent_size: int=2,
                         use_spaces: bool=True,):
        """
        :param max_line_length: Maximum number of characters for a line.
        :param cpplint_ignore:  List of checkers to ignore.
        :param cpplint_include: List of checkers to explicitly enable.
        :param use_spaces:      Only spaces are supported, hence a `True`
                                value.
        :param indent_size:     Only an indent size of 2 is permitted by
                                the bear.
        """
        check_invalid_config(use_spaces, indent_size)

        ignore = ','.join('-'+part.strip() for part in cpplint_ignore)
        include = ','.join('+'+part.strip() for part in cpplint_include)
        return ('--filter=' + ignore + ',' + include,
                '--linelength=' + str(max_line_length),
                filename)
