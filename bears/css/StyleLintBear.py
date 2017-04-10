import json
from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(executable='stylelint',
        output_format='regex',
        output_regex=r'\s*(?P<filename>.+)\s*(?P<line>\d+):(?P<column>\d+)\s*'
                     r'(\D)\s*(?P<message>.+)',
        config_suffix='.json')
class StyleLintBear:
    """
    Checks the code with stylelint. This will run stylelint over each file
    separately.

    Detect errors and potential problems in CSS code and to enforce
    appropriate coding conventions. For example, problems like syntax errors,
    invalid color codes etc can be detected.

    For more information on the analysis visit <http://stylelint.io/>
    """
    LANGUAGES = {'CSS', 'SCSS'}
    REQUIREMENTS = {NpmRequirement('stylelint', '7')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Unused Code', 'Formatting'}

    @staticmethod
    def generate_config(filename, file):
        # Use standard stylelint rules
        rules = {
            'at-rule-name-case': 'lower',
            'at-rule-name-space-after': 'always-single-line',
            'at-rule-semicolon-newline-after': 'always',
            'block-closing-brace-empty-line-before': 'never',
            'block-closing-brace-newline-after': 'always',
            'block-closing-brace-newline-before': 'always-multi-line',
            'block-closing-brace-space-before': 'always-single-line',
            'block-no-empty': True,
            'block-opening-brace-newline-after': 'always-multi-line',
            'block-opening-brace-space-after': 'always-single-line',
            'block-opening-brace-space-before': 'always',
            'color-hex-case': 'lower',
            'color-hex-length': 'short',
            'color-no-invalid-hex': True,
            'comment-no-empty': True,
            'comment-whitespace-inside': 'always',
            'declaration-bang-space-after': 'never',
            'declaration-bang-space-before': 'always',
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
            'value-list-max-empty-lines': 0
        }

        rules['at-rule-empty-line-before'] = [
             'always',
             {'except': ['blockless-after-same-name-blockless',
                         'first-nested'],
              'ignore': ['after-comment']}
        ]

        rules['comment-empty-line-before'] = [
         'always',
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

        default_config = {'rules': rules}
        return json.dumps(default_config)

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename, '--config=' + config_file
