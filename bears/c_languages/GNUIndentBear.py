import platform
import shlex
import sys

from coalib.bearlib import deprecate_settings
from coalib.bearlib.abstractions.Linter import linter
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


@linter(executable='indent' if platform.system() != 'Darwin' else 'gindent',
        use_stdin=True,
        output_format='corrected',
        result_message='Indentation can be improved.')
class GNUIndentBear:
    """
    This bear checks and corrects spacing and indentation via the well known
    Indent utility.

    C++ support is considered experimental.
    """

    LANGUAGES = {'C', 'CPP'}
    REQUIREMENTS = {DistributionRequirement('indent')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}

    @staticmethod
    @deprecate_settings(indent_size='tab_width')
    def create_arguments(filename, file, config_file,
                         max_line_length: int = 79,
                         use_spaces: bool = True,
                         blank_lines_after_declarations: bool = False,
                         blank_lines_after_procedures: bool = False,
                         blank_lines_after_commas: bool = False,
                         braces_on_if_line: bool = False,
                         braces_on_func_def_line: bool = False,
                         cuddle_else: bool = False,
                         while_and_brace_on_same_line: bool = False,
                         case_indentation: int = 0,
                         space_before_semicolon_after_empty_loop: bool = True,
                         delete_optional_blank_lines: bool = True,
                         declaration_indent: int = 0,
                         brace_indent: int = 2,
                         gnu_style: bool = False,
                         k_and_r_style: bool = False,
                         linux_style: bool = False,
                         indent_size: int = SpacingHelper.DEFAULT_TAB_WIDTH,
                         indent_cli_options: str = '',
                         ):
        """
        :param max_line_length:
            Maximum number of characters for a line.
            When set to 0, infinite line length is allowed.
        :param use_spaces:
            True if spaces are to be used, else tabs.
        :param blank_lines_after_declarations:
            Forces blank lines after the declarations.

            Example: If ``blank_lines_after_declarations = True`` then::

                int a;
                return ...;

            changes to::

                int a;

                return ...;

        :param blank_lines_after_procedures:
            Force blank lines after procedure bodies.
        :param blank_lines_after_commas:
            Forces newline after comma in declaration.

            Example: If ``blank_lines_after_commas = True`` then::

                int a, b;

            changes to::

                int a,
                b;

        :param braces_on_if_line:
            Puts the brace ``{`` on same line with if.

            Example: If ``braces_on_if_line = True``  then::

                if (x > 0)
                {

            changes to::

                if (x > 0) {

        :param braces_on_func_def_line:
            Puts the brace `{` on same line with the function declaration.
        :param cuddle_else:
            Cuddle else and preceding ``}``.

            Example: If ``cuddle_else = True`` then::

                if (...) {
                    ....
                }
                else {

            changes to::

                if (...) {
                    ....
                } else {

        :param while_and_brace_on_same_line:
            Cuddles while of ``do {} while``; and preceding ``}``.
        :param case_indentation:
            Specifies the number of spaces by which ``case`` in the ``switch``
            are indented.
        :param space_before_semicolon_after_empty_loop:
            Forces a blank before the semicolon ``;`` on one-line ``for`` and
            ``while`` statements.
        :param delete_optional_blank_lines:
             Deletes blank lines that are not needed. An example of needed
             blank line, is the blank line following a declaration when
             ``blank_line_after_declaration=True``.
        :param declaration_indent:
            Forces variables names to be aligned in column ``n`` with
            ``n = declaration_indent``  in declaration.

            Example: If ``declaration_indent = 8`` then::

                int a;
                float b;

            changes to::

                int     a;
                float   b;

        :param brace_indent:
            Specifies the number of spaces by which braces are indented. Its
            default value is 2.
        :param gnu_style:
            Uses GNU coding style.
        :param k_and_r_style:
            Uses Kernighan & Ritchie coding style.
        :param linux_style:
            Uses Linux coding style.
        :param indent_size:
            Number of spaces per indentation level.
        :param indent_cli_options:
            Any command line options the indent binary understands. They
            will be simply passed through.
        """
        # The limit is set to an arbitrary high value
        if not max_line_length:
            max_line_length = sys.maxsize

        indent_options = ('--no-tabs' if use_spaces else '--use-tabs',
                          '--line-length', str(max_line_length),
                          '--indent-level', str(indent_size),
                          '--tab-size', str(indent_size), )
        indent_options += (('--cuddle-do-while',)
                           if while_and_brace_on_same_line
                           else ('--dont-cuddle-do-while',))
        indent_options += (('--swallow-optional-blank-lines',)
                           if delete_optional_blank_lines else ('-nsob',))
        indent_options += (('--blank-lines-after-declarations',)
                           if blank_lines_after_declarations else ('-nbad',))
        indent_options += (('--blank-lines-after-commas',)
                           if blank_lines_after_commas else ('-nbc',))
        indent_options += (('--blank-lines-after-procedures',)
                           if blank_lines_after_procedures else ('-nbap',))
        indent_options += (('-di' + str(declaration_indent),)
                           if declaration_indent != 0 else ())
        indent_options += (('--case-indentation'+str(case_indentation),)
                           if case_indentation != 0 else ())
        indent_options += (('--space-special-semicolon',)
                           if space_before_semicolon_after_empty_loop
                           else ('-nss',))
        indent_options += ('--brace-indent'+str(brace_indent),)
        indent_options += (('--braces-on-func-def-line',)
                           if braces_on_func_def_line else ('-blf',))
        indent_options += ((('-ce',) if cuddle_else else ('-nce',)) +
                           ('-br',)) if braces_on_if_line else ('-bl',)
        indent_style_option = ()
        indent_style_option += ('--gnu-style',) if gnu_style else ()
        indent_style_option += (('--k-and-r-style',)
                                if k_and_r_style and indent_style_option is ()
                                else ())
        indent_style_option += (('--linux-style',)
                                if linux_style and indent_style_option is ()
                                else ())

        # If a style is chosen the other configs aren't passed to `indent`
        return (indent_style_option if indent_style_option is not ()
                else indent_options) + tuple(shlex.split(indent_cli_options))
