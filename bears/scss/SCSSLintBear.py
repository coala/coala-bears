import yaml

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GemRequirement import GemRequirement
from dependency_management.requirements.PipRequirement import PipRequirement


@linter(executable='scss-lint', output_format='regex',
        output_regex=r'.+:(?P<line>\d+)\s+(\[(?P<severity>.)\])\s*'
                     r'(?P<message>.*)')
class SCSSLintBear:
    """
    Check SCSS code to keep it clean and readable.

    More information is available at <https://github.com/brigade/scss-lint>.
    """

    LANGUAGES = {'SCSS'}
    REQUIREMENTS = {GemRequirement('scss-lint', '', 'false'),
                    PipRequirement('pyyaml', '3.12')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename, '--config', config_file

    @staticmethod
    def generate_config(filename, file,
                        space_around_bang: list=[True, False],
                        allow_chained_classes: bool=False,
                        prefer_color_keywords: bool=False,
                        use_color_variables: bool=True,
                        allow_debug_statement: bool=False,
                        check_declaration_order: bool=True,
                        allow_duplicate_properties: bool=False,
                        allow_consecutives_duplicate_property: bool=False,
                        else_on_same_line: bool=True,
                        force_empty_line_between_blocks: bool=True,
                        allow_empty_rules: bool=False,
                        use_short_hexadecimal_length_style: bool=True,
                        use_lowercase_hexadecimal: bool=True,
                        validate_hexadecimal: bool=True,
                        allow_id_selector: bool=False,
                        allow_important_rule_in_properties: bool=False,
                        use_spaces: bool=True,
                        indent_size: int=2,
                        exclude_leading_zero: bool=True,
                        allow_mergeable_selectors: bool=False,
                        allow_leading_underscore: bool=True,
                        function_naming_convention: str='hyphen',
                        mixin_naming_convention: str='hyphen',
                        variable_naming_convention: str='hyphen',
                        placeholder_naming_convention: str='hyphen',
                        max_nesting_depth: int=3,
                        use_placeholder_selector_in_extend: bool=True,
                        max_properties: int=10,
                        allow_unit_on_zero_values: bool=False,
                        check_ulrs_format: bool=True,
                        urls_in_quotes: bool=True,
                        allow_unnecesseary_parent_reference: bool=False,
                        allow_unnecessary_mantissa: bool=False,
                        allow_trailing_whitespaces: bool=False,
                        allow_trailing_semicolon: bool=True,
                        check_imports_path: bool=True,
                        allow_filename_leading_underscore: bool=False,
                        allow_filename_extension: bool=False,
                        use_length_variables: bool=True,
                        check_properties_spelling: bool=True,
                        extra_properties: list=(),
                        disabled_properties: list=(),
                        check_pseudo_elements: bool=True,
                        spaces_between_parentheses: int=0,
                        spaces_around_operators: str=1):
        """
        :param space_around_bang:
            Enforces a space before and/or after ``!`` (the "bang").
        :param allow_chained_classes:
            Allows defining a rule set using a selector with chained classes.
        :param prefer_color_keywords:
            Prefers color keywords over hexadecimal color codes.
        :param use_color_variables:
            Prefers color literals (keywords or hexadecimal codes) to be used
            only in variable declarations.
        :param allow_debug_statement:
            Allows ``@debug`` statements.
        :param check_declaration_order:
            Rule sets should be ordered as follows: ``@extend`` declarations,
            ``@include`` declarations without inner ``@content``, properties,
            ``@include`` declarations with inner ``@content``, then nested rule
            sets.
        :param allow_duplicate_properties:
            Allows defining the same property twice in a single rule set.
        :param allow_consecutives_duplicate_property:
            Allows defining the same property consecutively in a single rule
            set.
        :param else_on_same_line:
            Places ``@else`` statements on the same line as the preceding curly
            brace.
        :param force_empty_line_between_blocks:
            Separate rule, function, and mixin declarations with empty lines.
        :param allow_empty_rules:
            Allows empty rule set.
        :param use_short_hexadecimal_length_style:
            Prefer shorthand or long-form hexadecimal colors by setting the
            style option to short or long, respectively.
        :param use_lowercase_hexadecimal:
            Checks if hexadecimal colors are written in lowercase or uppercase.
        :param validate_hexadecimal:
            Ensure hexadecimal colors are valid (either three or six digits).
        :param allow_id_selector:
            Allows using ID selectors.
        :param allow_important_rule_in_property:
            Allows using ``!important`` in properties.
        :param use_spaces:
            Use spaces for indentation (tabs otherwise).
        :param indent_size:
            Number of spaces per indentation level.
        :param exclude_leading_zero:
            Determines whether leading zeros should be written or not in
            numeric values with a decimal point.
        :param allow_mergeable_selectors:
            Allows defining the same selector twice in a single sheet.
        :param allow_leading_underscore:
            Allows names to start with a single underscore.
        :param function_naming_convention:
            Name of convention (``hyphen``(use lowercase letters and hyphens)
            (default), ``camel``, ``snake``), or a ``regex`` the name must
            match (eg: ``^[a-zA-Z]+$``) to use for functions.
        :param mixin_naming_convention:
            Name of convention (``hyphen`` (default), ``camel``, ``snake``), or
            a regex the name must match (eg: ``^[a-zA-Z]+$``) to use for
            mixins.
        :param variable_naming_convention:
            Name of convention (``hyphen`` (default), ``camel``, ``snake``), or
            a regex the name must match (eg: ``^[a-zA-Z]+$``) to use for
            variables.
        :param placeholder_naming_convention:
            Name of convention (``hyphen`` (default), ``camel``, ``snake``), or
            a regex the name must match (eg: ``^[a-zA-Z]+$``) to use for
            placeholders.
        :param max_nesting_depth:
            Maximum nesting depth.
        :param use_placeholder_selector_in_extend:
            Enforces using placeholder selectors in ``@extend``.
        :param max_properties:
            Enforces a limit on the number of properties in a rule set.
        :param allow_unit_on_zero_values:
            Allow omitting length units on zero values.
        :param check_urls_format:
            URLs should be valid and not contain protocols or domain names.
        :param urls_in_quotes:
            URLs should always be enclosed within quotes.
        :param allow_unnecessary_parent_reference:
            Allows use of the parent selector references ``&`` even when they
            are not unnecessary.
        :param allow_unnecessary_mantissa:
            Numeric values can contain unnecessary fractional portions.
        :param allow_traling_whitespaces:
            Unables trailing whitespace.
        :param allow_trailing_semicolon:
            Property values; ``@extend``, ``@include``, and ``@import``
            directives; and variable declarations should always end with a
            semicolon.
        :param check_imports_path:
            The basenames of ``@import``ed SCSS partials should not begin with
            an underscore and should not include the filename extension.
            These requirements can be modified by changing
            ``allow_filename_leading_underscore``, and ``allow_extensions``.
        :param allow_filename_leading_underscore:
            Requires basenames of ``@import``ed SCSS partials to begin with an
            underscore.  This setting require ``check_import_paths`` to be
            enabled.
        :param allow_filename_extension:
            Requires basenames of ``@import``ed SCSS partials to include
            filename extension, this setting require ``check_import_paths`` to
            be enabled.
        :param use_length_variables:
            Prefer length literals (numbers with units) to be used only in
            variable declarations.

            ::
                 div {
                   width: 100px;
                 }

            Is not valid, whereas

            ::
                 $column-width: 100px;

                 div {
                   width: $column-width;
                 }
            is valid.
        :param check_properties_spelling:
            Reports when an unknown or disabled CSS property is used
            (ignoring vendor-prefixed properties).
        :param extra_properties:
            List of extra properties to allow.
        :param disabled_properties:
            List of existing properties to deny.
        :param check_pseudo_elements:
            Pseudo-elements, like ``::before``, and ``::first-letter``,
            should be declared with two colons. Pseudo-classes, like ``:hover``
            and ``:first-child``, should be declared with one colon.

            ::
                p::before {
                  content: '>'
                }

                p:hover {
                  color: red;
                }

        :param spaces_between_parentheses:
            Spaces to require between parentheses.
        :param spaces_around_operators:
            Operators should be formatted with a single space on both sides of
            an infix operator. The different value for this setting are ``1``,
            ``0`` or a number greater that ``1``.
        """
        naming_convention_map = {
            'camel': 'camel_case',
            'snake': 'snake_case',
            'hyphen': 'hyphenated_lowercase'
        }
        space_setting_map = {'one_space': 1, 'no_space': 0}
        options = {'BangFormat': {'enabled': True,
                                  'space_before_bang': space_around_bang[0],
                                  'space_after_bang': space_around_bang[1]},
                   'ChainedClasses': {'enabled': not allow_chained_classes},
                   'ColorKeyword': {'enabled': not prefer_color_keywords},
                   'ColorVariable': {'enabled': use_color_variables},
                   'DebugStatement': {'enabled': not allow_debug_statement},
                   'DeclarationOrder': {'enabled': check_declaration_order},
                   'DuplicateProperty': {
                       'enabled': not allow_duplicate_properties,
                       'ignore_consecutive':
                           allow_consecutives_duplicate_property},
                   'ElsePlacement': {'enabled': True,
                                     'style': ('same_line' if else_on_same_line
                                               else '')},
                   'EmptyLineBetweenBlocks': {
                       'enabled': force_empty_line_between_blocks,
                       'ignore_single_line_blocks': True},
                   'EmptyRule': {'enabled': not allow_empty_rules},
                   'HexLength': {'enabled': True,
                                 'style': ('short'
                                           if
                                           use_short_hexadecimal_length_style
                                           else 'long')},
                   'HexNotation': {'enabled': True,
                                   'style': ('lowercase'
                                             if use_lowercase_hexadecimal
                                             else 'uppercase')},
                   'HexValidation': {'enabled': validate_hexadecimal},
                   'IdSelector': {'enabled': not allow_id_selector},
                   'ImportantRule': {'enabled':
                                     not allow_important_rule_in_properties},
                   'Indentation': {'enabled': True,
                                   'allow_non_nested_indentation': False,
                                   'character': ('space'
                                                 if use_spaces else 'tab'),
                                   'width': indent_size},
                   'LeadingZero': {
                                   'enabled': True,
                                   'style': (
                                       'exclude_zero' if exclude_leading_zero
                                        else 'include_zero')
                                  },
                   'MergeableSelector': {'enabled': allow_mergeable_selectors,
                                         'force_nesting': True},
                   'NestingDepth': {'enabled': True,
                                    'max_depth': max_nesting_depth,
                                    'ignore_parent_selectors': False},
                   'NameFormat': {
                       'enabled': True,
                       'allow_leading_underscore': allow_leading_underscore,
                       'function_convention':
                           naming_convention_map.get(
                               function_naming_convention,
                               function_naming_convention),
                       'mixin_convention': naming_convention_map.get(
                           mixin_naming_convention, mixin_naming_convention),
                       'variable_convention':
                           naming_convention_map.get(
                               variable_naming_convention,
                               variable_naming_convention),
                       'placeholder_convention':
                           naming_convention_map.get(
                              placeholder_naming_convention,
                              placeholder_naming_convention)},
                   'PlaceholderInExtend': {
                       'enabled': use_placeholder_selector_in_extend},
                   'PropertyCount': {'enabled': False,
                                     'include_nested': False,
                                     'max_properties': max_properties},
                   'ZeroUnit': {'enabled': not allow_unit_on_zero_values},
                   'UrlFormat': {'enabled': check_ulrs_format},
                   'UrlQuotes': {'enabled': urls_in_quotes},
                   'UnnecessaryMantissa': {
                       'enabled': not allow_unnecessary_mantissa},
                   'UnnecessaryParentReference': {
                       'enabled': not allow_unnecesseary_parent_reference},
                   'TrailingSemicolon': {'enabled': allow_trailing_semicolon},
                   'TrailingWhitespace': {
                       'enabled': not allow_trailing_whitespaces},
                   'ImportPath': {
                       'enabled': check_imports_path,
                       'leading_underscore': allow_filename_leading_underscore,
                       'filename_extension': allow_filename_extension},
                   'LengthVariable': {'enabled': use_length_variables},
                   'PropertySpelling': {
                       'enabled': check_properties_spelling,
                       'extra_properties': extra_properties,
                       'disabled_properties': disabled_properties},
                   'SpaceBetweenParens': {'enabled': True,
                                          'spaces':
                                          spaces_between_parentheses},
                   'SpaceAroundOperator': {
                       'enabled': True,
                       'style': space_setting_map.get(spaces_around_operators,
                                                      'at_least_one_space')}}
        configs = {'linters': options}
        return yaml.dump(configs, default_flow_style=False)
