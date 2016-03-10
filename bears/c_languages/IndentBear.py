import platform

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.LocalBear import LocalBear


class IndentBear(Lint, LocalBear):
    executable = "indent" if platform.system() != "Darwin" else "gindent"
    diff_message = "Indentation can be improved."
    use_stdin = True
    gives_corrected = True

    def run(self,
            filename,
            file,
            max_line_length: int=80,
            use_spaces: bool=True,
            tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            indent_cli_options: str=''):
        """
        This bear checks and corrects spacing and indentation via the well
        known Indent utility. It is designed to work with the C programming
        language but may work reasonably with syntactically similar languages.

        :param max_line_length:    Maximum number of characters for a line.
        :param use_spaces:         True if spaces are to be used, else tabs.
        :param tab_width:          Number of spaces per indent level.
        :param indent_cli_options: Any command line options the indent binary
                                   understands. They will be simply passed
                                   through.
        """
        arguments = ("--no-tabs" if use_spaces else "--use-tabs",
                     "--line-length", str(max_line_length),
                     "--indent-level", str(tab_width),
                     "--tab-size", str(tab_width), str(indent_cli_options))
        return self.lint(arguments, file=file)
