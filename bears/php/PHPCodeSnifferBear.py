from coalib.bearlib.abstractions.Linter import linter
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)
from dependency_management.requirements.AnyOneOfRequirements import (
    AnyOneOfRequirements)
from dependency_management.requirements.ComposerRequirement import (
    ComposerRequirement)


@linter(executable='phpcs',
        output_format='regex',
        config_suffix='.xml',
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+): '
                     r'\w+ - (?P<message>.+)')
class PHPCodeSnifferBear:
    """
    Ensures that your PHP, JavaScript or CSS code remains clean and consistent.

    See <https://github.com/squizlabs/PHP_CodeSniffer> for more information.
    """

    LANGUAGES = {'PHP', 'JavaScript', 'CSS'}
    REQUIREMENTS = {
        AnyOneOfRequirements(
            [DistributionRequirement(apt_get='php-codesniffer',
                                     zypper='php-pear-php_codesniffer',
                                     ),
             ComposerRequirement('squizlabs/php_codesniffer'),
             ],
        ),
    }
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax', 'Documentation',
                  'Code Simplification'}
    ASCIINEMA_URL = 'https://asciinema.org/a/efawv96vdalck73tc3hwcabov'

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--report=emacs', '--standard='+config_file, filename

    @staticmethod
    def generate_config(filename, file,
                        max_line_length: int=79,
                        line_ending_character: str='\\n',
                        indent_size: int=SpacingHelper.DEFAULT_TAB_WIDTH,
                        use_spaces: bool=True,
                        allow_multiple_statements_per_line: bool=False,
                        force_lower_case_keywords: bool=True,
                        force_lower_case_constants: bool=True,
                        blank_line_after_namespace_declaration: bool=True,
                        check_use_blocks: bool=True,
                        check_class_declaration: bool=True,
                        check_property_declaration: bool=True,
                        force_scope_modifier_on_method: bool=True,
                        function_declaration_argument_spacing: int=1,
                        allow_multiline_function_declaration: bool=True):
        """
        :param max_line_length:
            Maximum number of characters for a line.
        :param line_ending_character:
            Checks that end of line characters correspond to the one provided.
        :param indent_size:
            Number of spaces per indentation level.
        :param use_spaces:
            True if spaces are to be used instead of tabs.
        :param allow_multiple_statements_per_line:
            Allows having multiple statements on one line.
        :param force_lower_case_keyword:
            Checks that ``PHP`` keywords are lowercase.
        :param force_lower_case_constant:
            Checks that all uses of ``true``, ``false`` and ``null`` are
            lowercase.
        :param blank_line_after_namespace_declaration:
            Ensures that there is a blank line after a namespace declaration.
        :param check_use_blocks:
            Ensures that there is one blank line after a ``use`` block,
            that there is only one use block per line, and that all ``use``
            declaration are done after namespaces declaration.
        :param check_class_declaration:
            Ensures that ``extends`` and ``implements`` keywords are declared
            on the same line as the class name, that the opening brace for a
            class is on the next line, and that the closing brace for a class
            is on the next line after the body. Allows splitting implements
            list accross multiple lines.
        :param check_property_declaration:
            Ensures that visibility is declared on all properties, that the
            ``var`` keyword is not used to declare a property, that there is
            not more that one property declared on a line, that properties are
            not prefixed with an underscore.
        :param force_scope_modifier_on_method:
            Verifies that class methods have scope modifiers.
        :param function_declaration_argument_spacing:
            Number of spaces between arguments in function declaration.
        :param allow_multiline_function_declaration:
            Allows argument lists to be split accross multiple lines correctly
            indented.
        """
        rules_map = {'Generic.WhiteSpace.DisallowTabIndent':
                     use_spaces,
                     'Generic.Formatting.DisallowMultipleStatements':
                     not allow_multiple_statements_per_line,
                     'Generic.PHP.LowerCaseKeyword':
                     force_lower_case_keywords,
                     'Generic.PHP.LowerCaseConstant':
                     force_lower_case_constants,
                     'PSR2.Namespaces.UseDeclaration':
                     check_use_blocks,
                     'PSR2.Namespaces.NamespaceDeclaration':
                     blank_line_after_namespace_declaration,
                     'PSR2.Classes.ClassDeclaration':
                     check_class_declaration,
                     'PSR2.Classes.PropertyDeclaration':
                     check_property_declaration,
                     'Squiz.Scope.MethodScope':
                     force_scope_modifier_on_method,
                     'Squiz.Functions.MultiLineFunctionDeclaration':
                     allow_multiline_function_declaration}
        rules = ''
        for k, v in rules_map.items():
            rules += '<rule ref="{}"/>\n'.format(k) if v else ''
        configs = '''<?xml version="1.0"?>
<ruleset name="Custom Standard">
 <description>A custom coding standard</description>
 <!-- Include the whole PSR-1 standard -->
 <rule ref="PSR1"/>
 <rule ref="Generic.Files.LineLength">
  <properties>
   <property name="lineLimit" value="{max_line_length}"/>
  </properties>
 </rule>
 <rule ref="Generic.Files.LineEndings">
  <properties>
   <property name="eolChar" value="{line_ending_character}"/>
  </properties>
 </rule>
 <rule ref="Generic.WhiteSpace.ScopeIndent">
  <properties>
   <property name="ignoreIndentationTokens" type="array"
   value="T_COMMENT,T_DOC_COMMENT_OPEN_TAG"/>
  </properties>
  <properties>
   <property name="indent" value="{indent_size}"/>
  </properties>
  <properties>
   <property name="exact" value="true"/>
  </properties>
 </rule>
 {some_rules}
 <rule ref="Squiz.WhiteSpace.ScopeKeywordSpacing"/>
 <rule ref="Squiz.Functions.FunctionDeclarationArgumentSpacing">
  <properties>
   <property name="equalsSpacing"
   value="{function_declaration_argument_spacing}"/>
  </properties>
 </rule>
 <rule
 ref="Squiz.Functions.FunctionDeclarationArgumentSpacing.SpacingAfterHint">
  <severity>0</severity>
 </rule>
</ruleset>
'''.format(max_line_length=max_line_length,
           line_ending_character=line_ending_character,
           indent_size=indent_size,
           some_rules=rules,
           function_declaration_argument_spacing=(
               function_declaration_argument_spacing))
        return configs
