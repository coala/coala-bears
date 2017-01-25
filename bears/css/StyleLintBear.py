import json

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(
    executable='stylelint',
    output_format='regex',
    output_regex=r'\s*(?P<filename>.+)\s*(?P<line>\d+):(?P<column>\d+)\s*'
                 r'(\D)\s*(?P<message>.+)',
    config_suffix='.json')
class StyleLintBear:
    """
    Helps to enforce consistent conventions and avoid errors in your
    stylesheets.

    Check <https://stylelint.io> for more information.
    """
    LANGUAGES = {'CSS', 'SCSS'}
    REQUIREMENTS = {NpmRequirement('stylelint', '7')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax', 'Code Simplification',
                  'Documentation', 'Duplication', 'Variable Misuse'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename, '--config', config_file

    @staticmethod
    def generate_config(filename, file,
                        hex_color_case: str='lower',
                        hex_color_length: str='short',
                        allow_invalid_hex: bool=False,
                        allow_empty_line_before_block_closing_brace:
                            bool=False,
                        enforce_newline_after_block_closing_brace: bool=True,
                        enforce_newline_before_multiline_block_closing_brace:
                            bool=True,
                        enforce_space_before_single_line_block_closing_brace:
                            bool=True,
                        allow_empty_block: bool=False,
                        enforce_newline_after_multiline_block_opening_brace:
                            bool=True,
                        enforce_space_after_single_line_block_opening_brace:
                            bool=True,
                        enforce_space_before_block_opening_brace: bool=True,
                        enforce_empty_line_before_comment: bool=True,
                        allow_empty_comment: bool=False,
                        comment_whitespace_inside_markers: bool=True,
                        ):
        """
        :param hex_color_case:
            Specify lowercase or uppercase for hex colors.
        :param hex_color_length:
            Specify short or long notation for hex colors.
        :param allow_invalid_hex:
            Specify whether or not invalid hexadecimal should be allowed.
        :param allow_empty_line_before_block_closing_brace:
            Require or disallow an empty line before the closing brace of
            blocks.
        :param enforce_newline_after_block_closing_brace:
            Require a newline after the closing brace of blocks.
        :param enforce_newline_before_multiline_block_closing_brace:
            Require a newline before the closing brace of multiline blocks.
        :param allow_empty_block:
            Allow or disallow empty block.
        :param enforce_newline_after_multiline_block_opening_brace:
             Require a newline after the opening brace of multiline blocks.
        :param enforce_space_after_single_line_block_opening_brace:
            Require a single space or disallow whitespace after the opening
            brace of single line blocks.
        :param enforce_space_before_block_opening_brace:
            Require a single space or disallow whitespace before the opening
            brace of blocks.
        :param enforce_empty_line_before_comment:
            Require or disallow an empty line before comments.
        :param allow_empty_comment:
            Allow or disallow empty comments.
        :param comment_whitespace_inside_markers:
            Require or disallow whitespace on the inside of comment markers.
        """
        rules = {
            'at-rule-name-case': 'lower',
            'at-rule-name-space-after': 'always-single-line',
            'at-rule-semicolon-newline-after': 'always',
            'block-closing-brace-empty-line-before': (
                 'never'
                 if not allow_empty_line_before_block_closing_brace
                 else 'always-multi-line'),
            'block-closing-brace-newline-after': (
                 'always'
                 if enforce_newline_after_block_closing_brace
                 else 'never-single-line'),
            'block-closing-brace-newline-before': (
                 'always-multi-line'
                 if enforce_newline_before_multiline_block_closing_brace
                 else 'never-multi-line'),
            'block-closing-brace-space-before': (
                 'always-single-line'
                 if enforce_space_before_single_line_block_closing_brace
                 else 'never-single-line'),
            'block-no-empty': not allow_empty_block,
            'block-opening-brace-newline-after': (
                 'always-multi-line'
                 if enforce_newline_after_multiline_block_opening_brace
                 else 'never-multi-line'),
            'block-opening-brace-space-after': (
                 'always-single-line'
                 if enforce_space_after_single_line_block_opening_brace
                 else 'never-single-line'),
            'block-opening-brace-space-before': (
                 'always'
                 if enforce_space_before_block_opening_brace else 'never'),
            'color-hex-case': hex_color_case,
            'color-hex-length': hex_color_length,
            'color-no-invalid-hex': not allow_invalid_hex,
            'declaration-block-no-redundant-longhand-properties': True,
            'declaration-block-no-shorthand-property-overrides': True,
            'declaration-block-semicolon-newline-after': 'always-multi-line',
            'declaration-block-semicolon-space-after': 'always-single-line',
            'declaration-block-semicolon-space-before': 'never',
            'declaration-block-single-line-max-declarations': 1,
            'declaration-block-trailing-semicolon': 'always',
            'declaration-colon-newline-after': 'always-multi-line',
            'declaration-colon-space-after': 'always-single-line',
            'declaration-colon-space-before': 'never',
            'font-family-no-duplicate-names': True,
            'function-calc-no-unspaced-operator': True,
            'function-comma-newline-after': 'always-multi-line',
            'function-comma-space-after': 'always-single-line',
            'function-comma-space-before': 'never',
            'function-linear-gradient-no-nonstandard-direction': True,
            'function-max-empty-lines': 0,
            'function-name-case': 'lower',
            'function-parentheses-newline-inside': 'always-multi-line',
            'function-parentheses-space-inside': 'never-single-line',
            'function-whitespace-after': 'always',
            'indentation': 2,
            'keyframe-declaration-no-important': True,
            'length-zero-no-unit': True,
            'max-empty-lines': 1,
            'media-feature-colon-space-after': 'always',
            'media-feature-colon-space-before': 'never',
            'media-feature-name-case': 'lower',
            'media-feature-name-no-unknown': True,
            'media-feature-parentheses-space-inside': 'never',
            'media-feature-range-operator-space-after': 'always',
            'media-feature-range-operator-space-before': 'always',
            'media-query-list-comma-newline-after': 'always-multi-line',
            'media-query-list-comma-space-after': 'always-single-line',
            'media-query-list-comma-space-before': 'never',
            'no-empty-source': True,
            'no-eol-whitespace': True,
            'no-extra-semicolons': True,
            'no-invalid-double-slash-comments': True,
            'no-missing-end-of-source-newline': True,
            'number-leading-zero': 'always',
            'number-no-trailing-zeros': True,
            'property-case': 'lower',
            'property-no-unknown': True,
            'selector-attribute-brackets-space-inside': 'never',
            'selector-attribute-operator-space-after': 'never',
            'selector-attribute-operator-space-before': 'never',
            'selector-combinator-space-after': 'always',
            'selector-combinator-space-before': 'always',
            'selector-descendant-combinator-no-non-space': True,
            'selector-list-comma-newline-after': 'always',
            'selector-list-comma-space-before': 'never',
            'selector-max-empty-lines': 0,
            'selector-pseudo-class-case': 'lower',
            'selector-pseudo-class-no-unknown': True,
            'selector-pseudo-class-parentheses-space-inside': 'never',
            'selector-pseudo-element-case': 'lower',
            'selector-pseudo-element-colon-notation': 'double',
            'selector-pseudo-element-no-unknown': True,
            'selector-type-case': 'lower',
            'selector-type-no-unknown': True,
            'shorthand-property-no-redundant-values': True,
            'string-no-newline': True,
            'unit-case': 'lower',
            'unit-no-unknown': True,
            'value-list-comma-newline-after': 'always-multi-line',
            'value-list-comma-space-after': 'always-single-line',
            'value-list-comma-space-before': 'never',
            'value-list-max-empty-lines': 0,
            'declaration-bang-space-after': 'never',
            'declaration-bang-space-before': 'always',
            'comment-no-empty': not allow_empty_comment,
            'comment-whitespace-inside': (
                'always' if comment_whitespace_inside_markers else 'never'
            )}
        rules['at-rule-empty-line-before'] = [
            'always',
            {'except': ['blockless-after-same-name-blockless', 'first-nested'],
             'ignore': ['after-comment']}]
        rules['comment-empty-line-before'] = [
            'always' if enforce_empty_line_before_comment else 'never',
            {'except': ['first-nested'], 'ignore': ['stylelint-commands']}
        ]
        rules['custom-property-empty-line-before'] = [
                'always',
                {'except': ['after-custom-property', 'first-nested'],
                 'ignore': ['after-comment', 'inside-single-line-block']}
            ]
        rules['declaration-block-no-duplicate-properties'] = [
                True,
                {'ignore': ['consecutive-duplicates-with-different-values']}
            ]
        rules['declaration-empty-line-before'] = [
                'always',
                {'except': ['after-declaration', 'first-nested'],
                 'ignore': ['after-comment', 'inside-single-line-block']}
                 ]
        rules['rule-nested-empty-line-before'] = [
            'always-multi-line',
            {'except': ['first-nested'], 'ignore': ['after-comment']}
        ]
        rules['rule-non-nested-empty-line-before'] = [
            'always-multi-line',
            {'ignore': ['after-comment']}
        ]
        configs = {'rules': rules}
        return json.dumps(configs, indent=2)
