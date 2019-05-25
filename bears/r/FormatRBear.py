from coala_utils.string_processing.Core import escape
from coalib.bearlib import deprecate_settings
from coalib.bearlib.abstractions.Linter import linter
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from dependency_management.requirements.AnyOneOfRequirements import (
    AnyOneOfRequirements)
from dependency_management.requirements.RscriptRequirement import (
    RscriptRequirement)
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


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
    LANGUAGES = {'R'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    REQUIREMENTS = {
        AnyOneOfRequirements(
            [DistributionRequirement(
                apt_get='r-cran-formatr',
                zypper='R-formatR',
             ),
             RscriptRequirement('formatR',
                                version='>1.5'),
             ]
        )
    }
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/0y0oxtak18v492jdyfqwpw1n4'
    CAN_FIX = {'Formatting'}

    @staticmethod
    @deprecate_settings(indent_size='tab_width')
    def create_arguments(filename, file, config_file,
                         r_keep_comments: bool = True,
                         r_keep_blank_lines: bool = True,
                         r_braces_on_next_line: bool = None,
                         r_use_arrows: bool = None,
                         indent_size:
                             int = SpacingHelper.DEFAULT_TAB_WIDTH,
                         r_max_expression_length: int = 0,
                         ):
        """
        :param r_keep_comments:
            Determines whether comments are kept or not.
        :param r_keep_blank_lines:
            Determines whether blank lines are kept or not.
        :param r_braces_on_next_line:
            Determines whether a brace should be placed on the next line.

            Example:
            If ``True``::

                if (...) {

            changes to::

                if (...)
                {

            If ``False`` the brace is placed on the same line.
        :param r_use_arrows:
            Determines whether the assignment operator ``=`` should be replaced
            by an arrow ``<-`` or not.

            Example: If  ``True``, ``x = 1`` changes to ``x <- 1``.
        :param indent_size:
            Number of spaces per indentation level.
        :param r_max_expression_length:
            Maximum number of characters for an expression.

            Example: If ``20`` then::

                1 + 1 + 1 + 1 + 1 + 1 + 1

            changes to::

                1 + 1 + 1 + 1 + 1 + 1 +
                    1
        """
        options = {'source="' + escape(filename, '"\\') + '"',
                   'blank=' + _map_to_r_bool(r_keep_blank_lines),
                   'comment=' + _map_to_r_bool(r_keep_comments),
                   'indent=' + str(indent_size)}
        if r_max_expression_length:
            options.add('width.cutoff=' + str(r_max_expression_length))
        if r_braces_on_next_line is not None:
            options.add('brace.newline=' +
                        _map_to_r_bool(r_braces_on_next_line))
        if r_use_arrows is not None:
            options.add('arrow=' + _map_to_r_bool(r_use_arrows))

        rcode = 'library(formatR);formatR::tidy_source({})'.format(
            ','.join(options))
        return '-e', rcode
