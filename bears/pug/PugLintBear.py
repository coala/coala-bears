import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import typed_list

from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(executable='pug-lint',
        output_format='regex',
        output_regex=r'(?P<line>\d+):?(?P<column>\d+)? (?P<message>.+)',
        use_stdout=False,
        use_stderr=True)
class PugLintBear:
    """
    A configurable linter and style checker for ``Pug`` (formerly ``Jade``)
    that is a clean, whitespace-sensitive template language for writing HTML.
    """

    LANGUAGES = {'Pug'}
    REQUIREMENTS = {NpmRequirement('pug-lint', '2.4.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax', 'Redundancy'}
    SEE_MORE = 'https://github.com/pugjs/pug-lint'

    @staticmethod
    def generate_config(filename, file,
                        prohibit_block_expansion: bool=True,
                        prohibit_class_attribute_with_static_value: bool=True,
                        prohibit_class_literals_before_attributes: bool=True,
                        prohibit_class_literals_before_id_literals: bool=True,
                        prohibit_class_literals: bool=True,
                        prohibit_duplicate_attributes: bool=True,
                        prohibit_html_text: bool=True,
                        prohibit_id_attribute_with_static_value: bool=True,
                        prohibit_id_literals_before_attributes: bool=True,
                        prohibit_id_literals: bool=True,
                        prohibit_legacy_mixin_call: bool=True,
                        prohibit_multiple_line_breaks: bool=False,
                        prohibit_spaces_inside_attribute_brackets: bool=True,
                        prohibit_string_interpolation: bool=True,
                        prohibit_tag_interpolation: bool=True,
                        prohibit_specific_attributes: typed_list(str)=None,
                        prohibit_specific_tags: typed_list(str)=None,
                        enforce_class_literals_before_attributes: bool=False,
                        enforce_class_literals_before_id_literals: bool=False,
                        enforce_id_literals_before_attributes: bool=False,
                        enforce_lower_case_attributes: bool=True,
                        enforce_lower_case_tags: bool=True,
                        enforce_spaces_inside_attribute_brackets: bool=False,
                        enforce_strict_equality_operators: bool=True,
                        validate_div_tags: bool=True,
                        validate_extensions: bool=True,
                        validate_self_closing_tags: bool=True,
                        preferred_quotation: str="'",
                        max_lines_per_file: int=None,
                        puglint_config: str=''):
        """
        :param prohibit_block_expansion:
            When ``True``, disallow any block expansion operators.
            For example: If set to ``True``, this will throw a warning::

                p: strong text
                table: tr: td text

        :param prohibit_class_attribute_with_static_value:
            When ``True``, prefer class literals over class attributes with
            static values.
            For example: If set to ``True``, prefer ``span.foo`` over
            ``span(class='foo')``.
        :param prohibit_class_literals_before_attributes:
            When ``True``, prefer all attribute blocks to be written before
            any class literals.
            For example: If set to ``True``, prefer
            ``input(type='text').class`` over ``input.class(type='text')``.
        :param prohibit_class_literals_before_id_literals:
            When ``True``, prefer all ID literals to be written before any
            class literals.
            For example: If set to ``True``, prefer
            ``input#id.class(type='text')`` over
            ``input.class#id(type='text')``.
        :param prohibit_class_literals:
            When ``True``, disallow any class literals.
            For example: If set to ``True``, prefer ``div(class='class')``
            over ``.class``.
        :param prohibit_duplicate_attributes:
            When ``True``, attribute blocks should not contain any duplicates.
            For example: If set to ``True``, this will throw a warning::

                div(a='a' a='b')
                #id(id='id')

        :param prohibit_html_text:
            When ``True``, disallow any HTML text.
            For example: If set to ``True``, this will throw a warning::

                <strong>html text</strong>
                p this is <strong>html</strong> text

        :param prohibit_id_attribute_with_static_value:
            When ``True``, prefer ID literals over ``id`` attributes with
            static values.
            For example: If set to ``True``, prefer ``span#id`` over
            ``span(id='foo')``.
        :param prohibit_id_literals_before_attributes:
            When ``True``, prefer all attribute blocks to be written before
            any ID literals.
            For example: If set to ``True``, prefer ``input(type='text')#id``
            over ``input#id(type='text')``.
        :param prohibit_id_literals:
            When ``True``, disallow any ID literals.
            For example: If set to ``True``, ``#id`` will throw a warning.
        :param prohibit_legacy_mixin_call:
            When ``True``, disallow any legacy mixin call.
            When ``True``, prefer ``+myMixin(arg)`` over
            ``mixin myMixin(arg)``.
        :param prohibit_multiple_line_breaks:
            When ``True``, disallow multiple blank lines in a row.
        :param prohibit_spaces_inside_attribute_brackets:
            When ``True``, disallow space after opening attribute bracket and
            before closing attribute bracket.
            For example: If set to ``True``, prefer
            ``input(type='text' name='name' value='value')`` over
            ``input( type='text' name='name' value='value' )``.
        :param prohibit_string_interpolation:
            When ``True``, disallow any string interpolation operators.
            For example: If set to ``True``, ``h1 #{title} text`` will throw
            a warning.
        :param prohibit_tag_interpolation:
            When ``True``, disallow any tag interpolation operators.
            For example: If set to ``True``, this will throw a warning::

                | #[strong html] text
                p #[strong html] text

        :param prohibit_specific_attributes:
            Disallow any of the attributes specified.
        :param prohibit_specific_tags:
            Disallow any of the tags specified.
        :param enforce_class_literals_before_attributes:
            When ``True``, all class literals must be written before any
            attribute blocks.
        :param enforce_class_literals_before_id_literals:
            When ``True``, all class literals should be written before any
            ID literals.
        :param enforce_id_literals_before_attributes:
            When ``True``, all ID literals must be written before any
            attribute blocks.
        :param enforce_lower_case_attributes:
            When ``True``, all attributes should be written in lower case.
            For example: If set to ``True``, prefer ``div(class='class')``
            over ``div(Class='class')``.
        :param enforce_lower_case_tags:
            When ``True``, all tags must be written in lower case.
            For example: If set to ``True``, prefer ``div(class='class')``
            over ``Div(class='class')``.
        :param enforce_spaces_inside_attribute_brackets:
            When ``True``, enforce space after opening attribute bracket and
            before closing attribute bracket.
        :param enforce_strict_equality_operators:
            When ``True``, enforce the use of ``===`` and ``!==`` instead of
            ``==`` and ``!=``.
        :param validate_div_tags:
            When ``True``, disallow any unnecessary ``div`` tags.
        :param validate_extensions:
            When ``True``, enforce proper file extensions with inclusion and
            inheritance.
        :param validate_self_closing_tags:
            When ``True``, disallow any unnecessary self closing tags.
        :param preferred_quotation:
            Your preferred quotation character, e.g.``"`` or ``'``.
        :param max_lines_per_file:
            Number of lines allowed per file.
        """
        if puglint_config:
            return None
        else:
            options = {
                'disallowBlockExpansion': prohibit_block_expansion,
                'disallowClassAttributeWithStaticValue':
                    prohibit_class_attribute_with_static_value,
                'disallowClassLiteralsBeforeAttributes':
                    prohibit_class_literals_before_attributes,
                'disallowClassLiteralsBeforeIdLiterals':
                    prohibit_class_literals_before_id_literals,
                'disallowClassLiterals': prohibit_class_literals,
                'disallowDuplicateAttributes': prohibit_duplicate_attributes,
                'disallowHtmlText': prohibit_html_text,
                'disallowIdAttributeWithStaticValue':
                    prohibit_id_attribute_with_static_value,
                'disallowIdLiteralsBeforeAttributes':
                    prohibit_id_literals_before_attributes,
                'disallowIdLiterals': prohibit_id_literals,
                'disallowLegacyMixinCall': prohibit_legacy_mixin_call,
                'disallowMultipleLineBreaks': prohibit_multiple_line_breaks,
                'disallowSpacesInsideAttributeBrackets':
                    prohibit_spaces_inside_attribute_brackets,
                'disallowStringInterpolation': prohibit_string_interpolation,
                'disallowTagInterpolation': prohibit_tag_interpolation,
                'disallowSpecificAttributes': prohibit_specific_attributes,
                'disallowSpecificTags': prohibit_specific_tags,
                'requireClassLiteralsBeforeAttributes':
                    enforce_class_literals_before_attributes,
                'requireClassLiteralsBeforeIdLiterals':
                    enforce_class_literals_before_id_literals,
                'requireIdLiteralsBeforeAttributes':
                    enforce_id_literals_before_attributes,
                'requireLowerCaseAttributes': enforce_lower_case_attributes,
                'requireLowerCaseTags': enforce_lower_case_tags,
                'requireSpacesInsideAttributeBrackets':
                    enforce_spaces_inside_attribute_brackets,
                'requireStrictEqualityOperators':
                    enforce_strict_equality_operators,
                'validateDivTags': validate_div_tags,
                'validateExtensions': validate_extensions,
                'validateSelfClosingTags': validate_self_closing_tags,
                'validateAttributeQuoteMarks': preferred_quotation,
                'maximumNumberOfLines': max_lines_per_file
            }

            for k, v in options.items():
                options[k] = v if v else None

            return json.dumps(options)

    @staticmethod
    def create_arguments(filename, file, config_file, puglint_config: str=''):
        """
        :param puglint_config:
            The location of a custom ``.pug-lintrc`` config file.
        """
        return ('--config',
                puglint_config if puglint_config else config_file,
                '--reporter', 'inline', filename)
