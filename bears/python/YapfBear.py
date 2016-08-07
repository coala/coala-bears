import sys

from yapf.yapflib.yapf_api import FormatFile

from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.bears.LocalBear import LocalBear
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.misc.ContextManagers import prepare_file
from coalib.results.Result import Result
from coalib.results.Diff import Diff


class YapfBear(LocalBear):
    """
    Check and correct formatting of Python code using ``yapf`` utility.

    See <https://github.com/google/yapf> for more information.
    """
    LANGUAGES = {"Python", "Python 2", "Python 3"}
    AUTHORS = {'The coala developers'}
    REQUIREMENTS = {PipRequirement('yapf', '0.10')}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}

    # TODO Add coalesce_brackets once supported by yapf
    def run(self, filename, file,
            max_line_length: int=79,
            tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            allow_multiline_lambdas: bool=False,
            blank_line_before_nested_class_or_def: bool=False,
            continuation_tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            dedent_closing_brackets: bool=False,
            indent_dictionary_value: bool=False,
            join_multiple_lines: bool=True,
            spaces_around_power_operator: bool=True,
            spaces_before_comment: int=2,
            space_between_ending_comma_and_closing_bracket: bool=False,
            split_arguments_when_comma_terminated: bool=False,
            split_before_bitwise_operator: bool=False,
            split_before_first_argument: bool=False,
            split_before_logical_operator: bool=False,
            split_before_named_assigns: bool=True,
            use_spaces: bool=True,
            based_on_style: str='pep8'):
        """
        :param max_line_length:
            Maximum number of characters for a line.
        :param tab_width:
            Number of spaces per indent level.
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
        """

        options = """
[style]
indent_width = {tab_width}
column_limit = {max_line_length}
allow_multiline_lambdas = {allow_multiline_lambdas}
continuation_indent_width = {continuation_tab_width}
dedent_closing_brackets = {dedent_closing_brackets}
indent_dictionary_value = {indent_dictionary_value}
join_multiple_lines = {join_multiple_lines}
spaces_around_power_operator = {spaces_around_power_operator}
spaces_before_comment = {spaces_before_comment}
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
        options += 'use_tabs = ' + str(not use_spaces)
        options = options.format(**locals())

        with prepare_file(options.splitlines(keepends=True),
                          None) as (file_, fname):
            corrected = FormatFile(filename,
                                   style_config=fname)[0].splitlines(True)
        diffs = Diff.from_string_arrays(file, corrected).split_diff()
        for diff in diffs:
            yield Result(self,
                         "The code does not comply with the settings "
                         "provided.",
                         affected_code=(diff.range(filename),),
                         diffs={filename: diff})

    @classmethod
    def check_prerequisites(cls):  # pragma: no cover
        if not sys.version_info >= (3, 4):
            return 'Yapf only supports Python 2.7 and Python 3.4+'
        else:
            return True
