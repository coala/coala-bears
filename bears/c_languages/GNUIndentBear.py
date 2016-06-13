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
                         blank_lines_after_declarations: bool=False,
                         blank_lines_after_procedures: bool=False,
                         blank_lines_after_commas: bool=False,
                         ignore_newlines: bool=True,
                         braces_on_if_line: bool=False,
                         braces_on_func_def_line: bool=False,
                         cuddle_else: bool=False,
                         cuddle_do_while: bool=False,
                         case_indentation: int=0,
                         space_special_semicolon: bool=True,
                         declaration_indent: int=0,
                         brace_indent: bool = False,
                         continue_at_parentheses: bool=True,
                         continuation_indentation: int=0,
                         gnu_style: bool=False,
                         k_and_r_style: bool=False,
                         linux_style: bool=False,
                         tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
                         indent_cli_options: str=''):
        """
        :param max_line_length:
            Maximum number of characters for a line.
        :param use_spaces:
            True if spaces are to be used, else tabs.
        :param blank_lines_after_declarations:
            Forces blank lines after the declarations.
        :param blank_lines_after_procedures:
            Force blank lines after procedure bodies.
        :param braces_on_if_line:
            Puts the brace ``{`` on same line with if.

            Example: If ``True``,
            ```
            if (x > 0)
            {
            ```
            changes to
            ```
            if (x > 0) {
            ```
        :param braces_on_func_def_line:
            Puts the brace `{` on same line with the function declaration.
        :param cuddle_else:
            Cuddle else and preceding ``}``.

            Example: If ``True``,
            ```
            if (...) {
                ....
            }
            else {
            ```
            changes to
            ```
            if (...) {
                ....
            } else {
            ```

        :param cuddle_do_while:
            Cuddles while of ``do {} while``; and preceding ``}``.
        :param space_special_semicolon:
            Forces a blank before the semicolon ``;`` on one-line ``for`` and
            ``while`` statements
        :param blank_lines_after_commas:
            Forces newline after comma in declaration.
        :param ignore_newlines:
            Does not break long lines at the position of newlines in the input
            file.
        :param declaration_indent:
            Puts variables in column (declaration_indent).
        :param brace_indent:
            Indents braces (brace_indent) spaces.
        :param continue_at_parentheses:
            Lines up continued lines at parentheses.
        :param continuation_indentation:
            Continuation indent of (continuation_indentation) spaces.
        :param gnu_style:
            Uses GNU coding style.
        :param k_and_r_style:
            Uses Kernighan & Ritchie coding style.
        :param linux_style:
            Uses Linux coding style.
        :param tab_width:
            Number of spaces per indent level.
        :param indent_cli_options:
            Any command line options the indent binary understands. They
            will be simply passed through.
        """
        indent_options = ("--no-tabs" if use_spaces else "--use-tabs",
                          "--line-length", str(max_line_length),
                          "--indent-level", str(tab_width),
                          "--continuation-indentation" +
                          str(continuation_indentation),
                          "--tab-size", str(tab_width), )
        indent_options += (("--cuddle-do-while",) if cuddle_do_while
                           else ("--dont-cuddle-do-while",))
        indent_options += (("--ignore-newlines",) if ignore_newlines
                           else ("--swallow-optional-blank-lines",))
        indent_options += (("--blank-lines-after-declarations",)
                           if blank_lines_after_declarations else ("-nbad",))
        indent_options += (("--blank-lines-after-commas",)
                           if blank_lines_after_commas else ("-nbc",))
        indent_options += (("--blank-lines-after-procedures",)
                           if blank_lines_after_procedures else ("-nbap",))
        indent_options += (("--continue-at-parentheses",)
                           if continue_at_parentheses else ("-nlp"))
        indent_options += (("-di" + str(declaration_indent),)
                           if declaration_indent != 0 else ())
        indent_options += (("--case-indentation"+str(case_indentation),)
                           if case_indentation != 0 else ())
        indent_options += (("--space-special-semicolon",)
                           if space_special_semicolon else ("-nss",))
        indent_options += ("--brace-indent",) if brace_indent else ()
        indent_options += ("--gnu-style",) if gnu_style else ()
        indent_options += ("--k-and-r-style",) if k_and_r_style else ()
        indent_options += ("--linux-style",) if linux_style else ()
        indent_options += (("--braces-on-func-def-line",)
                           if braces_on_func_def_line else ("-blf",))
        if braces_on_if_line:
            indent_options += (("-ce",)
                               if cuddle_else else ("-nce",)) + ("-br",)
        else:
            indent_options += ("--braces-after-if-line",)
        return indent_options + tuple(split(indent_cli_options))
