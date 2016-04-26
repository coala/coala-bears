from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import typed_list


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

    LANGUAGES = "C++"

    @staticmethod
    def create_arguments(filename, file, config_file,
                         max_line_length: int=80,
                         cpplint_ignore: typed_list(str)=(),
                         cpplint_include: typed_list(str)=()):
        """
        :param max_line_length: Maximum number of characters for a line.
        :param cpplint_ignore:  List of checkers to ignore.
        :param cpplint_include: List of checkers to explicitly enable.
        """
        ignore = ','.join('-'+part.strip() for part in cpplint_ignore)
        include = ','.join('+'+part.strip() for part in cpplint_include)
        return ('--filter=' + ignore + ',' + include,
                '--linelength=' + str(max_line_length),
                filename)
