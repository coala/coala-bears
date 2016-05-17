import platform
from shlex import split

from coalib.bearlib.abstractions.Linter import linter
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper


@linter(executable="indent" if platform.system() != "Darwin" else "gindent",
        use_stdin=True,
        output_format='corrected',
        result_message="Indentation can be improved.")
class GNUIndentBear:
    """
    This bear checks and corrects spacing and indentation via the well known
    Indent utility.

    C++ support is considered experimental.
    """

    LANGUAGES = ("C", "C++")

    @staticmethod
    def create_arguments(filename, file, config_file,
                         max_line_length: int=80,
                         use_spaces: bool=True,
                         tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
                         indent_cli_options: str=''):
        """
        :param max_line_length:    Maximum number of characters for a line.
        :param use_spaces:         True if spaces are to be used, else tabs.
        :param tab_width:          Number of spaces per indent level.
        :param indent_cli_options: Any command line options the indent binary
                                   understands. They will be simply passed
                                   through.
        """
        return ("--no-tabs" if use_spaces else "--use-tabs",
                "--line-length", str(max_line_length),
                "--indent-level", str(tab_width),
                "--tab-size", str(tab_width)) + tuple(split(indent_cli_options))
