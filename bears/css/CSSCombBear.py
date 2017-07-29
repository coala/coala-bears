from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.NpmRequirement import NpmRequirement
import json


@linter(executable='csscomb',
        output_format='corrected',
        use_stdin=True,
        result_message='Change coding style based on CSS rules')
class CSSCombBear:
    """
    CSScomb is a coding style formatter for CSS. You can easily write your own
    configuration to make your style sheets beautiful and consistent.

    For more information, consult <https://github.com/csscomb/csscomb.js>.
    """

    LANGUAGES = {"CSS"}
    REQUIREMENTS = {NpmRequirement('csscomb')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/bxpke7nizyxdf6mlx6ss4h405'
    CAN_FIX = {'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         remove_empty_rulesets: bool = True,
                         force_semicolon: bool = True,
                         upper_case_hex: bool = True,
                         block_indent: str = "\t",
                         allow_shorthand_color: bool = False,
                         eof_newline: bool = True,
                         leading_zero: bool = True,
                         use_single_quotes: bool = True,
                         sort_order_fallback: bool = True,
                         space_before_colon: bool = True,
                         space_after_colon: bool = True,
                         space_between_declaration: str = "\n",
                         space_before_o_brace: bool = True,
                         space_after_o_brace: bool = True,
                         space_after_s_delim: bool = True,
                         space_before_c_brace: bool = True,
                         strip_spaces: bool = True,
                         use_spaces: bool = False,
                         vendor_prefix_align: bool = True):
        """
        :param filename
            The filename user wants to use.
        :param remove_empty_rulesets:
            Remove empty rulesets if they exist.

            Example:

            ::
                .a {
                    color: tomato;
                }
                .b{}

            After using the bear:

            ::
                .a {
                    color: tomato;
                }
        :param force_semicolon:
            If ``True``, adds a semicolon at the end.

            Example:

            ::
                .a {
                    color: tomato
                }

            After using the bear:

            ::
                .a {
                    color: tomato;
                }
        :param upper_case_hex:
            If ``True``, make characters for the color upper.

            Example(for upper case):

            ::
                .a {
                    color: #fff;
                }

            After using the bear:

            ::
                .a {
                    color: #FFF;
                }
        :param block_indent:
            If set to "\t", indents by a tab.
            If set to " ", indents by a space.
        :param allow_shorthand_color:
            If ``True``, changes the hexa colors into short form.

            Example(for True case):

            ::
                .a {
                    color: #ffcc00;
                }

            After using the bear:

            ::
                .a {
                    color: #fc0;
                }
        :param eof_newline:
            If ``True``, adds a newline at EOF.
        :param leading_zero:
            If ``False``, keeps the zeroes preceding the dots.
            If ``True``, adds the zeroes preceding the dots.

            Example(False case):
            .a {
                padding: 0.1vh;
                font-size: 0.5em;
            }

            After using the bear:
            .a {
                padding: .1vh;
                font-size: .5em;
            }
        :param use_single_quotes:
            If ``True``, use single quotes.
        :param sort_order_fallback:
            Sorts the properties alphabetically.
        :param space_before_colon:
            If ``True``, add a space before colon.
            If "", remove a space before colon.
        :param space_after_colon:
            If ``True``, adds a space after colon.
            If ``False``, remove a space after colon.
        :param space_between_declaration:
            If "\n", adds a line break between declarations.
        :param space_before_o_brace:
            If ``True``, adds a line break before opening brace.
        :param space_after_o_brace:
            If ``True``, adds a line break after opening brace.
        ::param space_after_s_delim
            If ``True``, adds a line break after selector delimiter

            Example:

            ::
                .a, .b{
                    color: tomato;
                }

            After using the bear:

            ::
                .a,
                .b{
                    color: tomato;
                }
        :param space_before_s_delim:
            If ``True``, adds a space before selector delimiter.
        :param space_before_c_brace:
            If "True", adds a line break before closing brace.
        :param strip_spaces:
            If ``True``, trim trailing spaces.
        :param use_spaces:
            If ``True``, use spaces as indent.
        :param vendor_prefix_align:
            If ``True``, align prefixes.

            Example:

            ::
                .a {
                    -webkit-border-radius: 3px;
                    -moz- border-radius: 3px;
                    border-radius: 3px;
                }

            After using the bear:

            ::
                .a {
                    -hebkit-border-radius: 3px;
                     -moz-border-radius: 3px;
                       border-radius: 3px;
                }
        :param csscomb_json:
            The path of the `.csscomb.json` config file.
            If this option is present, all of the above options
            are not used. Instead, the `.csscomb.json` file is
            used as the configuration file.
        """

        options = {"remove-empty-rulesets": remove_empty_rulesets,
                   "always-semicolon": force_semicolon,
                   "color-case": upper_case_hex,
                   "block-indent": block_indent,
                   "eof-newline": eof_newline,
                   "leading-zero": leading_zero,
                   "use_single_quotes": use_single_quotes,
                   "sort-order-fallback": sort_order_fallback,
                   "space-before-colon": space_before_colon,
                   "space-after-colon": space_after_colon,
                   "space-between-declarations": space_between_declaration,
                   "space-before-opening-brace": space_before_o_brace,
                   "space-after-opening-brace": space_after_o_brace,
                   "space-after-selector-delimiter": space_after_s_delim,
                   "space-before-closing-brace": space_before_c_brace,
                   "strip-spaces": strip_spaces,
                   "vendor-prefix-align": vendor_prefix_align
                   }
        if sort_order_fallback:
            options["sort-order-fallback"] = "abc"
        if space_before_o_brace:
            options["space-before-opening-brace"] = "\n"
        if space_after_o_brace:
            options["space-after-opening-brace"] = "\n"
        if space_before_colon:
            options["space-before-colon"] = " "
        if space_after_colon:
            options["space-after-colon"] = " "

        return json.dumps(options)
