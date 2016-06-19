from coalib.bearlib.abstractions.Linter import linter
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.parsing.StringProcessing import escape


def _map_to_r_bool(py_bool):
    return 'TRUE' if py_bool else 'FALSE'


@linter(executable='Rscript',
        output_format='corrected',
        prerequisite_check_command=('Rscript', '-e', 'library(formatR)'),
        prerequisite_check_fail_message='Please install formatR for this bear '
                                        'to work.')
class FormatRBear:
    """
    Check and correct formatting of R Code using known formatR utility.
    """
    LANGUAGES = {"R"}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         r_keep_comments: bool=True,
                         r_keep_blank_lines: bool=True,
                         r_braces_on_next_line: bool=False,
                         r_use_arrows: bool=False,
                         tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
                         r_max_expression_length: int=20):
        """
        :param r_keep_comments:
            Determines whether comments are kept or not.
        :param r_keep_blank_lines:
            Determines whether blank lines are kept or not.
        :param r_braces_on_next_line:
            Determines whether a brace should be placed on the next line.

            Example:
            If ``True``,
            ```
            if (...) {
            ```
            changes to
            ```
            if (...)
            {
            ```
            If ``False`` the brace is placed on the same line.
        :param r_use_arrows:
            Determines if either the assign operator ``=`` or the arrow ``<-``
            should be used.

            Example: If  ``True``, ``x = 1`` changes to ``x <- 1``.
        :param tab_width:
            Number of spaces for indentation.
        :param r_max_expression_length:
            Maximum number of characters for an expression.

            Example: If ``20`` then
            ```
            1 + 1 + 1 + 1 + 1 + 1 + 1
            ```
            changes to
            ```
            1 + 1 + 1 + 1 + 1 + 1 +
                1
            ```
        """
        rcode = ('library(formatR);'
                 'formatR::tidy_source('
                 'source="' + escape(filename, '"\\') + '",'
                 'comment={r_keep_comments},'
                 'blank={r_keep_blank_lines},'
                 'arrow={r_use_arrows},'
                 'brace.newline={r_braces_on_next_line},'
                 'indent='
                 '{tab_width}'.format(tab_width=tab_width,
                                      r_keep_comments=_map_to_r_bool(
                                          r_keep_comments),
                                      r_keep_blank_lines=_map_to_r_bool(
                                          r_keep_blank_lines),
                                      r_use_arrows=_map_to_r_bool(
                                          r_use_arrows),
                                      r_braces_on_next_line=_map_to_r_bool(
                                          r_braces_on_next_line)))
        # Disable r_max_expression_length if it is equal to 0
        rcode += ('' if r_max_expression_length == 0
                  else ',width.cutoff=' + str(r_max_expression_length)) + ')'
        return '-e', rcode
