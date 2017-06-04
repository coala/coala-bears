import json

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement

_setting_map = {True: 'always',
                False: 'never',
                None: 'false'}


@linter(executable='stylint',
        output_format='regex',
        output_regex=r'(?P<line>\d+):?(?P<column>\d+)?\s+.*?'
                     r'(?P<severity>error|warning)\s+(?P<message>.+?)'
                     r'(?:  .*|\n|$)')
class StylintBear:
    """
    Attempts to catch little mistakes (duplication of rules for instance) and
    enforces a code style guide on Stylus (a dynamic stylesheet language
    with the ``.styl`` extension that is compiled into CSS) files.

    The ``StylintBear`` is able to catch following problems:
    - Duplication of rules
    - Mixed spaces and tabs
    - Unnecessary brackets
    - Missing colon between property and value
    - Naming conventions
    - Trailing whitespace
    - Consistent quotation style
    - Use of extra spaces inside parenthesis
    - Naming convention when declaring classes, ids, and variables
    - Unnecessary leading zeroes on decimal points
    - Checks if a property is valid CSS or HTML
    """

    LANGUAGES = {'Stylus'}
    REQUIREMENTS = {NpmRequirement('stylint', '1.5.9')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax', 'Redundancy'}
    SEE_MORE = 'https://github.com/SimenB/stylint'

    @staticmethod
    def generate_config(filename, file,
                        block_keyword: bool=None,
                        brackets: bool=False,
                        colons_for_property_declaration: bool=True,
                        color_variables_for_hex_values: bool=True,
                        spaces_after_commas: bool=True,
                        spaces_after_comments: bool=True,
                        allow_trailing_whitespace: bool=False,
                        no_css_literals: bool=False,
                        max_selector_depth: bool=False,
                        check_duplicates: bool=True,
                        efficient_properties: bool=True,
                        extend_preference: str=None,
                        indent_size: int=0,
                        leading_zero: bool=None,
                        max_errors: int=0,
                        max_warnings: int=0,
                        mixed_spaces_and_tabs: bool=False,
                        variable_naming_convention: str=None,
                        strict_naming_convention: bool=False,
                        none_keyword: bool=False,
                        check_no_important_keyword: bool=True,
                        spaces_inside_parentheses: bool=None,
                        placeholder: bool=True,
                        prefix_vars_with_dollar: bool=True,
                        semicolons: bool=False,
                        sort_order: str='alphabetical',
                        stacked_properties: bool=False,
                        check_property_validity: bool=True,
                        preferred_quotation: str=None,
                        zero_units: bool=False,
                        z_index_normalize_base: int=0,
                        stylint_config: str=''):
        """
        :param block_keyword:
            When ``True`` expect the ``@block`` keyword when defining block
            variables. When ``False``, expect no ``@block`` keyword when
            defining block variables.
        :param brackets:
            When ``True``, expect ``{}`` when declaring a selector. When
            ``False``, expect no brackets when declaring a selector.
        :param colons_for_property_declaration:
            When ``True``, expect ``:`` when declaring a property. When
            ``False``, expect no ``:`` when declaring a property.
        :param color_variables_for_hex_values:
            When ``True``, enforce variables when defining hex values.
        :param spaces_after_commas:
            Enforce or disallow spaces after commas.
        :param spaces_after_comments:
            Enforce or disallow spaces after line comments.
            For example: If set to ``True``, prefer
            ``// comment`` over ``//comment``.
        :param allow_trailing_whitespace:
            If ``True``, ignores trailing whitespace. If ``False``, trailing
            whitespace will throw a warning.
        :param no_css_literals:
            By default Stylint ignores ``@css`` blocks. If set to ``True``
            however, warnings are thrown if ``@css`` is used.
        :param max_selector_depth:
            Set the max selector depth. If set to 4, max selector depth will
            be 4 indents. Pseudo selectors like ``&:first-child`` or
            ``&:hover`` won't count towards the limit.
        :param check_duplicates:
            Checks if selectors or properties are duplicated unnecessarily.
        :param efficient_properties:
            Check for places where properties can be written more efficiently.
        :param extend_preference:
            Pass in either ``@extend`` or ``@extends`` and then enforce that.
            Both are valid in Stylus. It doesn't really matter which one
            you use.
            For example: If set to ``@extends``, prefer
            ``@extends $some-var`` instead of ``@extend $some-var``
            or if set to ``@extend``, prefer
            ``@extend $some-var`` over ``@extends $some-var``.
        :param indent_size:
            This works in conjunction with ``max_selector_depth``. If you
            indent with spaces this is the number of spaces you indent with.
            If you use hard tabs, set this value to ``0``.
            For example: If set to ``2``, prefer
            ``/s/smargin: 0`` over ``/s/s/smargin: 0``.
        :param leading_zero:
            When ``True``, prefer leading zeroes on decimal points. When
            ``False``, disallow leading zeroes on decimal points.
        :param max_errors:
            Set maximum number of errors. If ``0``, all errors will
            be shown without a limit.
        :param max_warnings:
            Set maximum number of warnings. If ``0``, all errors will
            be shown without a limit.
        :param mixed_spaces_and_tabs:
            If a non-negative number is passed to ``indent_size``,
            soft tabs (i.e. spaces) are assumed, and if
            ``0`` is passed to ``indent_size``, hard tabs are assumed.
            For example: If ``indent_size = 4`` and
            ``mixed_spaces_and_tabs = True``, prefer
            ``/s/s/s/smargin 0`` over ``/tmargin 0``
            or if ``indent_size = 0`` and
            ``mixed_spaces_and_tabs = True``, prefer
            ``/tmargin 0`` over ``/s/s/s/smargin 0``.
        :param variable_naming_convention:
            Enforce a particular naming convention when declaring variables.
            Throws a warning if you don't follow the convention.
            Supported values are ``lowercase-dash``, ``lowercase_underscore``,
            ``camelCase`` and ``BEM``.
        :param strict_naming_convention:
            By default, ``variable_naming_convention`` only looks at variable
            names. If ``strict_naming_convention`` is set to ``True``,
            ``variable_naming_convention`` will also look at class and
            ID names.
        :param none_keyword:
            If ``True`` check for places where ``none`` used instead of ``0``.
            If ``False`` check for places where ``0`` could be used
            instead of ``none``.
        :param check_no_important_keyword:
            If ``True``, show warning when ``!important`` is found.
            For example: If set to ``True``, this will throw a warning::

                div
                    color red !important

        :param spaces_inside_parentheses:
            Enforce or disallow use of extra spaces inside parentheses.
            For example: If set to ``True``, prefer
            ``my-mixin( $myParam )`` over ``my-mixin($myParam)``
            or if set to ``False``, prefer
            ``my-mixin($myParam)`` over ``my-mixin( $myParam )``.
        :param placeholder:
            Enforce extending placeholder vars when using ``@extend(s)``.
        :param prefix_vars_with_dollar:
            Enforce use of ``$`` when defining a variable. In Stylus, using a
            ``$`` when defining a variable is optional, but is a good idea
            if you want to prevent ambiguity. Not including the ``$`` sets up
            situations where you wonder: "Is this a variable or a value?"
            For instance: ``padding $default`` is easier to understand than
            ``padding default``.
            For example: If set to ``True``, prefer
            ``$my-var = 0`` over ``my-var = 0``
            or if set to ``False``, prefer
            ``my-var = 0`` over ``$my-var = 0``.
        :param semicolons:
            When ``True``, enforce semicolons. When ``False``, disallow
            semicolons.
        :param sort_order:
            Enforce a particular sort order when declaring properties. Throws
            a warning if you don't follow the order.
            For example: If set to ``alphabetical``, prefer this::

                .some-class
                    display block
                    float left
                    position absolute
                    right 10px
                    top 0

            over this::

                .some-class
                    position absolute
                    top 0
                    right 10px
                    display block
                    float left

            Supported values are ``alphabetical`` and ``grouped``.
        :param stacked_properties:
            No one-liners. Enforce putting properties on new lines.
            For example: If set to ``False``, prefer::

                .className
                    padding 0

            over
            ``.className { padding 0 }``
        :param check_property_validity:
            Check that a property is valid CSS or HTML.
        :param preferred_quotation:
            Your preferred quotation character, e.g. ``double`` or ``single``.
        :param zero_units:
            Looks for instances of ``0px``. You don't need the ``px``.
            Checks all units, not just ``px``.
        :param z_index_normalize_base:
            Enforce some basic z-index sanity. Any number passed in
            will be used as the base for your z-index values.
            Use ``0`` to disable this feature.
            For example: If set to ``5``, prefer
            ``z-index 10`` over ``z-index 9``
            or if set to ``10``, prefer
            ``z-index 20`` over ``z-index 15``.
        """
        if stylint_config:
            return None
        else:
            options = {
                'blocks': _setting_map[block_keyword],
                'brackets': _setting_map[brackets],
                'colons': _setting_map[colons_for_property_declaration],
                'colors': _setting_map[color_variables_for_hex_values],
                'commaSpace': _setting_map[spaces_after_commas],
                'commentSpace': _setting_map[spaces_after_comments],
                'cssLiteral': _setting_map[no_css_literals],
                'depthLimit': max_selector_depth,
                'duplicates': check_duplicates,
                'efficient': _setting_map[efficient_properties],
                'extendPref': extend_preference,
                'indentPref': indent_size,
                'leadingZero': _setting_map[leading_zero],
                'maxErrors': max_errors,
                'maxWarnings': max_warnings,
                'mixed': mixed_spaces_and_tabs,
                'namingConvention': variable_naming_convention,
                'namingConventionStrict': strict_naming_convention,
                'none': _setting_map[none_keyword],
                'noImportant': check_no_important_keyword,
                'parenSpace': _setting_map[spaces_inside_parentheses],
                'placeholders': _setting_map[placeholder],
                'prefixVarsWithDollar': _setting_map[prefix_vars_with_dollar],
                'quotePref': preferred_quotation,
                'semicolons': _setting_map[semicolons],
                'sortOrder': sort_order,
                'stackedProperties': _setting_map[stacked_properties],
                'trailingWhitespace':
                    False if allow_trailing_whitespace is True else 'never',
                'valid': check_property_validity,
                'zeroUnits': _setting_map[zero_units],
                'zIndexNormalize':
                    False if z_index_normalize_base == 0
                    else z_index_normalize_base,
                'groupOutputByFile': True,
                'reporterOptions': {
                    'columns': ['lineData', 'severity', 'description', 'rule'],
                    'columnSplitter': '  ',
                    'showHeaders': False,
                    'truncate': True
                }
            }

            return json.dumps(options)

    @staticmethod
    def create_arguments(filename, file, config_file, stylint_config: str=''):
        """
        :param stylint_config:
            The location of the ``.stylintrc`` config file.
        """
        return ('--config',
                stylint_config if stylint_config else config_file,
                filename)
