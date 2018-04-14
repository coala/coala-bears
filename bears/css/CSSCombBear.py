import json

from coalib.bearlib.abstractions.Linter import linter

from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(executable='csscomb',
        output_format='corrected',
        use_stdin=True,
        result_message='The text does not comply to the set style.')
class CSSCombBear:
    """
    CSScomb is a coding style formatter for CSS. You can easily write your own
    configuration to make your style sheets beautiful and consistent.
    """

    LANGUAGES = {'CSS'}
    REQUIREMENTS = {NpmRequirement('csscomb', '4.2.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/bxpke7nizyxdf6mlx6ss4h405'
    CAN_FIX = {'Formatting'}
    SEE_MORE = 'https://github.com/csscomb/csscomb.js'

    @staticmethod
    def generate_config(filename, file,
                        enforce_semicolon: bool = True,
                        use_block_indentation: int = 4,
                        use_color_case: str = 'upper',
                        allow_color_shorthand: bool = None,
                        allow_leading_zero_in_dimensions: bool = True,
                        preferred_quotation: str = "'",
                        prohibit_empty_rulesets: bool = True,
                        use_space_after_colon: int = 1,
                        use_space_before_colon: int = 0,
                        use_space_after_combinator: int = 1,
                        use_space_before_combinator: int = 1,
                        use_space_between_declarations: int = None,
                        use_space_after_opening_brace: int = None,
                        use_space_before_opening_brace: int = 1,
                        use_space_before_closing_brace: int = None,
                        use_space_after_selector_delimiter: int = 1,
                        use_space_before_selector_delimiter: int = 1,
                        prohibit_trailing_whitespace: bool = True,
                        prohibit_units_in_zero_valued_dimensions: bool = True,
                        vendor_prefix_align: bool = None,
                        use_lines_between_rulesets: int = 1,
                        csscomb_config: str = '',
                        ):
        """
        :param enforce_semicolon:
            Whether to add a semicolon after the last value/mixin.
            For example: If set to ``True``, prefer this::

                a { color: red; text-decoration: underline; }

            over this::

                a { color: red; text-decoration: underline }

        :param use_block_indentation:
            Set the number of spaces as indent for code inside blocks,
            including media queries and nested rules.
            For example: If set to ``4``, prefer this::

                a {
                    top: 0;
                    p {
                        color: tomato;
                        position: happy;
                        }
                    }

            over this::

                a {
                top: 0;
                  p {
                      color: tomato;
                position: happy;
                 }
                }

        :param use_color_case:
            Unify case of hexadecimal colors. Acceptable values are ``lower``
            and ``upper``.
            For example: If set to ``lower``, prefer this::

                a { color: #fff }

            over this::

                a { color: #FFF }

        :param allow_color_shorthand:
            Whether to expand hexadecimal colors or use shorthands.
            For example: If set to ``True``, prefer this::

                b { color: #fc0 }

            over this::

                b { color: #ffcc00 }

        :param allow_leading_zero_in_dimensions:
            Add/remove leading zero in dimensions.
            For example: If set to ``False``, prefer this::

                p { padding: .5em }

            over this::

                p { padding: 0.5em }

        :param preferred_quotation:
            ``'`` or ``"`` respectively.
        :param prohibit_empty_rulesets:
            Remove all rulesets that contain nothing but spaces.
            For example: If set to ``True``, prefer this::

                a { color: red; } p { /* hey */ }

            over this::

                a { color: red; } p { /* hey */ } b { }

        :param use_space_after_colon:
            Set the number of spaces after ``:`` in declarations.
            For example: If set to ``1``, prefer this::

                a {
                    top: 0;
                    color: tomato;
                }

            over this::

                a {
                    top:0;
                    color:tomato;
                }

        :param use_space_before_colon:
            Set the number of spaces before ``:`` in declarations.
            For example: If set to ``1``, prefer this::

                a {
                    top : 0;
                    color : tomato;
                }

            over this::

                a {
                    top: 0;
                    color: tomato;
                }

        :param use_space_after_combinator:
            Set the number of spaces after the combinator.
            For example: If set to ``1``, prefer this::

                p> a { color: panda; }

            over this::

                p>a { color: panda; }

        :param use_space_before_combinator:
            Set the number of spaces before the combinator.
            For example: If set to ``1``, prefer this::

                p >a { color: panda; }

            over this::

                p>a { color: panda; }

        :param use_space_between_declarations:
            Set the number of spaces between declarations.
        :param use_space_after_opening_brace:
            Set the number of spaces after ``{``.
        :param use_space_before_opening_brace:
            Set the number of spaces before ``{``.
        :param use_space_before_closing_brace:
            Set the number of spaces before ``}``.
        :param use_space_after_selector_delimiter:
            Set the number of spaces after the selector delimiter.
            For example: If set to ``1``, prefer this::

                a, b {
                    color: panda;
                    }

            over this::

                a,b{
                    color: panda;
                    }

        :param use_space_before_selector_delimiter:
            Set the number of spaces before selector delimiter.
        :param prohibit_trailing_whitespace:
            Whether to allow trailing whitespace or not.
        :param prohibit_units_in_zero_valued_dimensions:
            Whether to remove units in zero-valued dimensions.
            For example: If set to ``True``, prefer this::

                img { border: 0 }

            over this::

                img { border: 0px }

        :param vendor_prefix_align:
            Whether to align prefixes in properties and values.
            For example: If set to ``True``, prefer this::

            a
            {
                -webkit-border-radius: 3px;
                   -moz-border-radius: 3px;
                        border-radius: 3px;
                background: -webkit-linear-gradient(top, #fff 0, #eee 100%);
                background:    -moz-linear-gradient(top, #fff 0, #eee 100%);
            }

            over this::

            a
            {
                -webkit-border-radius: 3px;
                -moz-border-radius: 3px;
                border-radius: 3px;
                background: -webkit-linear-gradient(top, #fff 0, #eee 100%);
                background: -moz-linear-gradient(top, #fff 0, #eee 100%);
            }

        :param use_lines_between_rulesets:
            Number of line breaks between rulesets or ``@rules``.
        """
        if csscomb_config:
            return None
        else:
            options = {
                'always-semicolon': enforce_semicolon if enforce_semicolon
                else None,
                'block-indent': use_block_indentation,
                'color-case': use_color_case,
                'color-shorthand': allow_color_shorthand,
                'leading-zero': allow_leading_zero_in_dimensions,
                'quotes': 'single' if preferred_quotation == "'" else 'double',
                'remove-empty-rulesets': prohibit_empty_rulesets if
                prohibit_empty_rulesets else None,
                'space-after-colon': use_space_after_colon,
                'space-before-colon': use_space_before_colon,
                'space-after-combinator': use_space_after_combinator,
                'space-before-combinator': use_space_before_combinator,
                'space-between-declarations': use_space_between_declarations,
                'space-after-opening-brace': use_space_after_opening_brace,
                'space-before-opening-brace': use_space_before_opening_brace,
                'space-before-closing-brace': use_space_before_closing_brace,
                'space-after-selector-delimiter':
                    use_space_after_selector_delimiter,
                'space-before-selector-delimiter':
                    use_space_before_selector_delimiter,
                'strip-spaces': prohibit_trailing_whitespace if
                prohibit_trailing_whitespace else None,
                'unitless-zero': prohibit_units_in_zero_valued_dimensions if
                prohibit_units_in_zero_valued_dimensions else None,
                'vendor-prefix-align': vendor_prefix_align if
                vendor_prefix_align else None,
                'lines-between-rulesets': use_lines_between_rulesets
            }

            return json.dumps(options)

    @staticmethod
    def create_arguments(filename, file, config_file,
                         csscomb_config: str = '',
                         ):
        """
        :param csscomb_config:
            The location of the ``.csscomb.json`` config file.
        """
        return ('--config',
                csscomb_config if csscomb_config else config_file)
