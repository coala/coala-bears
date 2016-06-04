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
                         blank_lines_after_decl: bool=False,
                         blank_lines_after_proc: bool=True,
                         blank_lines_after_commas: bool=False,
                         ignore_newlines: bool = True,
                         declaration_indent: int=-1,
                         brace_indent: bool = False,
                         continue_at_parentheses: bool=True,
                         continuation_indentation: int=0,
                         swallow_optional_blank_lines: bool = False,
                         gnu_style: bool=False,
                         k_and_r_style: bool=False,
                         linux_style: bool=False,
                         tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
                         indent_cli_options: str=''):
        """
        :param max_line_length:              Maximum number of characters for
                                             a line.
        :param use_spaces:                   True if spaces are to be used,
                                             else tabs.
        :param blank_lines_after_decl:       Force blank lines after the
                                             declarations.
        :param blank_lines_after_proc:       Force blank lines after procedure
                                             bodies.
        :param blank_lines_after_commas:     Force newline after comma in
                                             declaration.
        :param ignore_newlines:              Do not break long lines at the
                                             position of newlines in the input
                                             file.
        :param declaration_indent:           Put variables in column
                                             (declaration_indent).
        :param brace_indent:                 Indent braces (brace_indent)
                                             spaces.
        :param continue_at_parentheses:      Line up continued lines at
                                             parentheses.
        :param continuation_indentation:     Continuation indent of
                                             (continuation_indentation) spaces.
        :param swallow_optional_blank_lines: Swallow optional blank lines.
        :param gnu_style:                    Use GNU coding style.
        :param k_and_r_style:                Use Kernighan & Ritchie coding
                                             style.
        :param linux_style:                  Use Linux coding style.
        :param tab_width:                    Number of spaces per indent level.
        :param indent_cli_options:           Any command line options the
                                             indent binary understands. They
                                             will be simply passed through.
        """
        indent_options = ("--no-tabs" if use_spaces else "--use-tabs",
                          "--line-length", str(max_line_length),
                          "--indent-level", str(tab_width),
                          "--continuation-indentation" +
                          str(continuation_indentation),
                          "--tab-size", str(tab_width), )
        if blank_lines_after_decl:
            indent_options += ("--blank-lines-after-declarations",)
        else:
            indent_options += ("--no-blank-lines-after-declarations",)
        if blank_lines_after_proc:
            indent_options += ("--blank-lines-after-procedures",)
        else:
            indent_options += ("--no-blank-lines-after-procedures",)
        if continue_at_parentheses:
            indent_options += ("--continue-at-parentheses",)
        else:
            indent_options += ("-nlp",)
        if blank_lines_after_commas:
            indent_options += ("--ignore-newlines",)
        if declaration_indent > -1:
            indent_options += ("--declaration-indentation" +
                               str(declaration_indent), )
        if brace_indent:
            indent_options += ("--brace-indent",)
        if gnu_style:
            indent_options += ("--gnu-style",)
        if k_and_r_style:
            indent_options += ("--k-and-r-style",)
        if linux_style:
            indent_options += ("--linux-style",)
        if swallow_optional_blank_lines:
            indent_options += ("--swallow-optional-blank-lines",)
        return indent_options + tuple(split(indent_cli_options))
