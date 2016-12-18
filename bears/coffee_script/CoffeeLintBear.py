import json

from coalib.bearlib import deprecate_settings
from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result
from coala_utils.param_conversion import negate


@linter(executable='coffeelint',
        use_stdin=True)
class CoffeeLintBear:
    """
    Check CoffeeScript code for a clean and consistent style.

    For more information about coffeelint, visit <http://www.coffeelint.org/>.
    """

    LANGUAGES = {'CoffeeScript'}
    REQUIREMENTS = {NpmRequirement('coffeelint', '1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting', 'Smell', 'Complexity', 'Duplication'}

    severity_map = {'warn': RESULT_SEVERITY.NORMAL,
                    'error': RESULT_SEVERITY.MAJOR,
                    'ignore': RESULT_SEVERITY.INFO}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--reporter=raw', '--stdin', '-f', config_file

    @staticmethod
    @deprecate_settings(indent_size='tab_width',
                        allow_increment=(
                            'no_decr_or_incrementation_operators', negate),
                        allow_no_parameters=(
                            'no_empty_parameter_list', negate),
                        allow_empty_functions=('no_empty_functions', negate),
                        allow_this_statements=('no_this', negate),
                        allow_implicit_parentheses=(
                            'no_implicit_parentheses', negate),
                        allow_interpolation_in_single_quotes=(
                            'no_interpolation_in_single_quotes', negate),
                        allow_stand_alone_at_sign=(
                            'no_stand_alone_at_sign', negate),
                        allow_throwing_strings=(
                            'disable_throwing_strings', negate),
                        allow_unnecessary_double_quotes=(
                            'no_unnecessary_double_quotes', negate),
                        allow_bitwise_operators=(
                            'use_english_operator', negate),
                        force_braces='no_implicit_braces')
    def generate_config(filename, file,
                        max_line_length: int=79,
                        max_line_length_affect_comments: bool=True,
                        space_before_and_after_arrow: bool=True,
                        check_braces_spacing: bool=False,
                        braces_spacing_width: int=1,
                        spacing_in_empty_braces: int=0,
                        class_naming_camelCase: bool=True,
                        spaces_before_and_after_colon: bool=False,
                        spaces_before_colon: int=0,
                        spaces_after_colon: int=1,
                        enforce_newline_at_EOF: bool=True,
                        use_spaces: bool=True,
                        indent_size: int=2,
                        number_of_newlines_after_classes: int=2,
                        prohibit_embedding_javascript_snippet: bool=True,
                        force_braces: bool=False,
                        allow_implicit_parentheses: bool=True,
                        allow_interpolation_in_single_quotes: bool=True,
                        allow_stand_alone_at_sign: bool=False,
                        allow_throwing_strings: bool=False,
                        allow_trailing_semicolons: bool=False,
                        allow_trailing_whitespaces: bool=False,
                        allow_unnecessary_double_quotes: bool=True,
                        allow_bitwise_operators: bool=True,
                        spaces_around_operators: bool=True,
                        space_after_comma: bool=True,
                        cyclomatic_complexity: int=0,
                        prevent_duplicate_keys: bool=True,
                        consistent_line_endings_style: str='',
                        allow_this_statements: bool=True,
                        allow_increment: bool=True,
                        allow_no_parameters: bool=True,
                        allow_empty_functions: bool=False,
                        enforce_parentheses_on_non_empty_constructors:
                            bool=True
                        ):
        """
        :param max_line_length:
            Maximum number of characters per line.
        :param max_line_length_affect_comments:
            Determines if ``max_line_length`` should also affects comments or
            not.
        :param space_before_and_after_arrow:
            Determines if spaces should be used before and after the arrow.
        :param check_braces_spacing:
            Checks if proper spacing is used inside curly braces.
        :param braces_spacing_width:
            Determines the number of blank spaces after the opening ``{`` and
            before the closing brace ``}`` given that there is something within
            the braces.
        :param spacing_in_empty_braces:
            Determines the number of blank spaces after the opening ``{`` and
            before the closing brace ``}`` given empty content.
        :param class_naming_camelCase:
            Checks whether the classes name should be in camel-case or not.
        :param spaces_before_and_after_colon:
            Checks the number of spaces before and after colon.
        :param spaces_before_colon:
            Determines the number of blank spaces before colon when
            ``spaces_before_and_after_colon == True``.
        :param spaces_after_colon:
            Determines the number of space after colon when
            ``spaces_before_and_after_colon == True``.
        :param enforce_newline_at_EOF:
            Checks if the file ends with a single newline.
        :param use_spaces:
            Forbids tabs in indentation and applies two spaces for this
            purpose.
        :param indent_size:
            Number of spaces per indentation level.
        :param number_of_newlines_after_classes:
            Determines the number of newlines that separate the class
            definition and the rest of the code.
        :param prohibit_embedding_javascript_snippet:
            Prevents some JavaScript elements like ``eval`` to affect
            CoffeeScript.
        :param force_braces:
            Prohibits implicit braces when declaring object literals.

            Example: If ``force_braces = True`` then
            ```
            1:2, 3:4
            ```
            is prohibited, whereas
            ```
            {1:2, 3:4}
            ```
            is accepted.
        :param allow_implicit_parentheses:
            Allows implicit parentheses.
        :param allow_interpolation_in_single_quotes:
            Allows string interpolation in a single quoted string.

            Example: If ``allow_interpolation_in_single_quotes = False`` then
            ```
            f = '#{bar}'
            ```
            is prohibited, whereas
            ```
            f = "#{bar}"
            ```
            is correct.
        :param allow_stand_alone_at_sign:
            Allows the use of stand alone  ``@``.

            Example: If ``allow_stand_alone_at_sign = False``
            ```
            @ notok
            not(@).ok
            @::
            ```
            are prohibited, whereas
            ```
            @alright
            @(fn)
            @ok()
            @[ok]
            @ok()
            ```
            are accepted.
        :param allow_throwing_strings:
            Allows throwing string literals or interpolation.

            Example: If ``allow_throwing_strings = False``
            ```
            throw 'my error'
            throw "#{1234}"
            ```
            will not be permitted.
        :param allow_trailing_semicolons:
            Prohibits trailing semicolons when ``False`` since they are
            not useful. The semicolon is meaningful only if there's another
            instruction on the same line.

            Example: If ``allow_trailing_semicolon = False``
            ```
            x = '1234'; console.log(x)
            ```
            Here the semicolon is meaningful.
            ```
            alert('end of line');
            ```
            This semicolon is redundant.
        :param allow_trailing_whitespaces:
            Checks whether to allow trailing whitespacess in the code or not.
        :param allow_unnecessary_double_quotes:
            Allows enclosing strings in double quotes.
        :param allow_bitwise_operators:
            Determines if ``and``, ``or``, ``is`` and ``isnt`` should be used
            instead of ``&&``, ``||``, ``==`` and ``!=``.
        :param spaces_around_operators:
            Enforces that operators have spaces around them.
        :param space_after_comma:
            Checks if there is a blank space after commas.
        :param cyclomatic_complexity:
            Maximum cyclomatic complexity of the file.
        :param prevent_duplicate_keys:
            Prevents defining duplicate keys in object literals and classes.
        :param enforce_parentheses_on_non_empty_constructors:
            Requires constructors with parameters to include parentheses.

            Example:
            ```
            class Foo
            # Warn about missing parentheses here
            a = new Foo
            b = new bar.foo.Foo
            # The parentheses make it clear no parameters are intended
            c = new Foo()
            d = new bar.foo.Foo()
            e = new Foo 1, 2
            f = new bar.foo.Foo 1, 2
            ```
        :param consistent_line_endings_style:
            The option to ``line_endings``, its value is either ``unix`` or
            ``windows``.
        :param allow_this_statements:
            Allows the use of ``this``. ``@`` should be used if ``False``.
        :param allow_increment:
            Allows the use of increment and decrement arithmetic operators.
        :param allow_no_parameters:
            Allows empty parameter lists in function definitions.
        :param allow_empty_functions:
            Allows declaring empty functions.
        """
        coffee_configs = {'max_line_length':
                          {'value': max_line_length,
                           'level': 'error',
                           'limitComments':
                               max_line_length_affect_comments}}
        coffee_configs['arrow_spacing'] = (
            {'level': 'error' if space_before_and_after_arrow else 'ignore'})
        if check_braces_spacing:
            coffee_configs['braces_spacing'] = (
                {'level': 'error',
                 'spaces': braces_spacing_width,
                 'empty_object_spaces': spacing_in_empty_braces})
        if class_naming_camelCase:
            coffee_configs['camel_case_classes'] = {'level': 'error'}
        if spaces_before_and_after_colon:
            coffee_configs['colon_assignment_spacing'] = (
                {'level': 'error',
                 'spacing': {'left': spaces_before_colon,
                             'right': spaces_after_colon}})
        coffee_configs['eol_last'] = (
            {'level': 'error' if enforce_newline_at_EOF else 'ignore'})
        coffee_configs['newlines_after_classes'] = (
            {'value': number_of_newlines_after_classes,
             'level': 'error'})
        coffee_configs['no_backticks'] = (
            {'level': 'error'
                if prohibit_embedding_javascript_snippet else 'ignore'})
        if force_braces:
            coffee_configs['no_implicit_braces'] = (
                {'level': 'error', 'strict': True})
        if not allow_implicit_parentheses:
            coffee_configs['no_implicit_parens'] = (
                {'strict': True, 'level': 'error'})
        coffee_configs['no_interpolation_in_single_quotes'] = (
            {'level': 'error'
                if not allow_interpolation_in_single_quotes else 'ignore'})
        if not allow_stand_alone_at_sign:
            coffee_configs['no_stand_alone_at'] = {'level': 'error'}
        if use_spaces:
            coffee_configs['no_tabs'] = {'level': 'error'}
        coffee_configs['indentation'] = (
            {'value': indent_size, 'level': 'error'})
        coffee_configs['no_throwing_strings'] = (
            {'level': 'error' if not allow_throwing_strings else 'ignore'})
        coffee_configs['no_trailing_semicolons'] = (
            {'level': 'error' if not allow_trailing_semicolons else 'ignore'})
        if not allow_trailing_whitespaces:
            coffee_configs['no_trailing_whitespace'] = (
                {'level': 'error',
                 'allowed_in_comments': True,
                 'allowed_in_empty_lines': True})
        if not allow_unnecessary_double_quotes:
            coffee_configs['no_unnecessary_double_quotes'] = {'level': 'error'}
        if not allow_bitwise_operators:
            coffee_configs['prefer_english_operator'] = (
                {'level': 'error', 'doubleNotLevel': 'ignore'})
        if spaces_around_operators:
            coffee_configs['space_operators'] = {'level': 'error'}
        if space_after_comma:
            coffee_configs['spacing_after_comma'] = {'level': 'warn'}
        coffee_configs['cyclomatic_complexity'] = (
                {'value': cyclomatic_complexity,
                 'level': ('error' if cyclomatic_complexity else 'ignore')})
        coffee_configs['duplicate_key'] = (
            {'level': 'error' if prevent_duplicate_keys else 'ignore'})
        if enforce_parentheses_on_non_empty_constructors:
            coffee_configs['non_empty_constructor_needs_parens'] = (
                {'level': 'error'})
        if consistent_line_endings_style:
            coffee_configs['line_endings'] = (
                {'level': 'error', 'value': consistent_line_endings_style})
        if not allow_this_statements:
            coffee_configs['no_this'] = {'level': 'error'}
        if not allow_increment:
            coffee_configs['no_plusplus'] = {'level': 'error'}
        coffee_configs['no_empty_param_list'] = (
            {'level': 'error' if not allow_no_parameters else 'ignore'})
        coffee_configs['no_empty_functions'] = (
            {'level': 'error' if not allow_empty_functions else 'ignore'})

        return json.dumps(coffee_configs)

    def process_output(self, output, filename, file):
        output = json.loads(output)

        assert len(output) == 1, (
            'More than 1 file parsed, something went wrong')
        for item in tuple(output.values())[0]:
            yield Result.from_values(
                origin='{} ({})'.format(self.name, item['rule']),
                message=item['message'],
                file=filename,
                line=item.get('lineNumber', None),
                end_line=item.get('lineNumberEnd', None),
                severity=self.severity_map[item['level']],
                additional_info=item.get('description',
                                         item.get('context', '')))
