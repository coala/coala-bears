from yapf.yapflib.yapf_api import FormatCode

from coalib.bearlib import deprecate_settings
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.LocalBear import LocalBear
from dependency_management.requirements.PipRequirement import PipRequirement
from coala_utils.ContextManagers import prepare_file
from coalib.results.Result import Result
from coalib.results.Diff import Diff


class YapfBear(LocalBear):
    LANGUAGES = {'Python', 'Python 2', 'Python 3'}
    AUTHORS = {'The coala developers'}
    REQUIREMENTS = {PipRequirement('yapf', '0.14.0')}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}
    ASCIINEMA_URL = 'https://asciinema.org/a/89021'

    @deprecate_settings(indent_size='tab_width')
    def run(self, filename, file,
            max_line_length: int=79,
            indent_size: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            allow_multiline_lambdas: bool=False,
            blank_line_before_nested_class_or_def: bool=False,
            continuation_tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            dedent_closing_brackets: bool=False,
            indent_dictionary_value: bool=False,
            coalesce_brackets: bool=False,
            join_multiple_lines: bool=True,
            spaces_around_power_operator: bool=True,
            spaces_before_comment: int=2,
            space_between_ending_comma_and_closing_bracket: bool=True,
            split_arguments_when_comma_terminated: bool=False,
            split_before_bitwise_operator: bool=False,
            split_before_first_argument: bool=False,
            split_before_logical_operator: bool=False,
            split_before_named_assigns: bool=True,
            use_spaces: bool=True,
            based_on_style: str='pep8',
            prefer_line_break_after_opening_bracket: bool=True):
        """
        Check and correct formatting of Python code using ``yapf`` utility.

        See <https://github.com/google/yapf> for more information.

        :param max_line_length:
            Maximum number of characters for a line.
        :param indent_size:
            Number of spaces per indentation level.
        :param allow_multiline_lambdas:
            Allows lambdas to be formatted on more than one line.
        :param blank_line_before_nested_class_or_def:
            Inserts a blank line before a ``def`` or ``class`` immediately
            nested within another ``def`` or ``class``.
        :param continuation_tab_width:
            Indent width used for line continuations.
        :param dedent_closing_brackets:
            Puts closing brackets on a separate line, dedented, if the
            bracketed expression can't fit in a single line. Applies to all
            kinds of brackets, including function definitions and calls.
        :param indent_dictionary_value:
            Indents the dictionary value if it cannot fit on the same line as
            the dictionary key.
        :param coalesce_brackets:
            Prevents splitting consecutive brackets. Only relevant when
            ``dedent_closing_brackets`` is set.
            Example:
            If ``True``::

                call_func_that_takes_a_dict(
                    {
                        'key1': 'value1',
                        'key2': 'value2',
                    }
                )

            would reformat to::

                call_func_that_takes_a_dict({
                    'key1': 'value1',
                    'key2': 'value2',
                })

        :param join_multiple_lines:
            Joins short lines into one line.
        :param spaces_around_power_operator:
            Set to ``True`` to prefer using spaces around ``**``.
        :param spaces_before_comment:
            The number of spaces required before a trailing comment.
        :param space_between_ending_comma_and_closing_bracket:
            Inserts a space between the ending comma and closing bracket of a
            list, etc.
        :param split_arguments_when_comma_terminated:
            Splits before arguments if the argument list is terminated by a
            comma.
        :param split_before_bitwise_operator:
            Set to ``True`` to prefer splitting before ``&``, ``|`` or ``^``
            rather than after.
        :param split_before_first_argument:
            If an argument / parameter list is going to be split, then split
            before the first argument.
        :param split_before_logical_operator:
            Set to ``True`` to prefer splitting before ``and`` or ``or`` rather
            than after.
        :param split_before_named_assigns:
            Splits named assignments into individual lines.
        :param use_spaces:
            Uses spaces for indentation.
        :param based_on_style:
            The formatting style to be used as reference.
        :param prefer_line_break_after_opening_bracket:
            If True, splitting right after a open bracket will not be
            preferred.
        """
        if not file:
            # Yapf cannot handle zero-byte files well, and adds a redundent
            # newline into the file. To avoid this, we don't parse zero-byte
            # files as they cannot have anything to format either.
            return

        options = """
[style]
indent_width = {indent_size}
column_limit = {max_line_length}
allow_multiline_lambdas = {allow_multiline_lambdas}
continuation_indent_width = {continuation_tab_width}
dedent_closing_brackets = {dedent_closing_brackets}
indent_dictionary_value = {indent_dictionary_value}
join_multiple_lines = {join_multiple_lines}
spaces_around_power_operator = {spaces_around_power_operator}
spaces_before_comment = {spaces_before_comment}
coalesce_brackets = {coalesce_brackets}
split_before_bitwise_operator = {split_before_bitwise_operator}
split_before_first_argument = {split_before_first_argument}
split_before_logical_operator = {split_before_logical_operator}
split_before_named_assigns = {split_before_named_assigns}
based_on_style = {based_on_style}
blank_line_before_nested_class_or_def = {blank_line_before_nested_class_or_def}
split_arguments_when_comma_terminated = {split_arguments_when_comma_terminated}
space_between_ending_comma_and_closing_bracket= \
{space_between_ending_comma_and_closing_bracket}
"""
        options += 'use_tabs = ' + str(not use_spaces) + '\n'
        options += ('split_penalty_after_opening_bracket = ' +
                    ('30' if prefer_line_break_after_opening_bracket
                     else '0') + '\n')
        options = options.format(**locals())

        try:
            with prepare_file(options.splitlines(keepends=True),
                              None) as (file_, fname):
                corrected = FormatCode(
                    ''.join(file), style_config=fname)[0].splitlines(True)
        except SyntaxError as err:
            if isinstance(err, IndentationError):
                error_type = 'indentation errors (' + err.args[0] + ')'
            else:
                error_type = 'syntax errors'
            yield Result.from_values(
                self,
                'The code cannot be parsed due to {0}.'.format(error_type),
                filename, line=err.lineno, column=err.offset)
            return
        diffs = Diff.from_string_arrays(file, corrected).split_diff()
        for diff in diffs:
            yield Result(self,
                         'The code does not comply with the settings '
                         'provided.',
                         affected_code=(diff.range(filename),),
                         diffs={filename: diff})
