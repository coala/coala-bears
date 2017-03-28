import json
import yaml

from coalib.bearlib import deprecate_settings
from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GemRequirement import GemRequirement
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


@linter(executable='rubocop',
        use_stdin=True)
class RuboCopBear:
    """
    Check Ruby code for syntactic, formatting as well as semantic problems.

    See <https://github.com/bbatsov/rubocop#cops> for more information.
    """

    LANGUAGES = {'Ruby'}
    REQUIREMENTS = {GemRequirement('rubocop', '0.47.1'),
                    PipRequirement('pyyaml', '3.12')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/39241'
    CAN_DETECT = {'Simplification'}
    CAN_FIX = {'Syntax', 'Formatting'}

    severity_map = {'error': RESULT_SEVERITY.MAJOR,
                    'warning': RESULT_SEVERITY.NORMAL,
                    'convention': RESULT_SEVERITY.INFO}

    @staticmethod
    def create_arguments(filename, file, config_file, rubocop_config: str=''):
        # Need both stdin and filename. Explained in this comment:
        # https://github.com/bbatsov/rubocop/pull/2146#issuecomment-131403694
        args = (filename, '--stdin', '--format=json')
        if rubocop_config:
            args += ('--config', rubocop_config)
        else:
            args += ('--config', config_file)
        return args

    @staticmethod
    @deprecate_settings(indent_size='tab_width',
                        method_length_count_comments='method_count_comments',
                        method_naming_convention='method_name_case',
                        variable_naming_convention='variable_name_case')
    def generate_config(filename, file,
                        access_modifier_indentation: str='indent',
                        preferred_alias: str='prefer_alias',
                        align_hash_rocket_by: str='key',
                        align_colon_by: str='key',
                        inspect_last_argument_hash: str='always_inspect',
                        align_parameters: str='with_first_parameter',
                        class_check: str='is_a?',
                        comment_keywords: tuple=('TODO',
                                                 'FIXME',
                                                 'OPTIMIZE',
                                                 'HACK',
                                                 'REVIEW'),
                        min_if_unless_guard: int=1,
                        indent_size: int=2,
                        method_naming_convention: str='snake',
                        string_literals: str='single_quotes',
                        variable_naming_convention: str='snake',
                        max_class_length: int=100,
                        class_length_count_comments: bool=False,
                        max_module_length: int=100,
                        module_length_count_comments: bool=False,
                        cyclomatic_complexity: int=6,
                        max_line_length: int=79,
                        line_length_allow_here_doc: bool=True,
                        line_length_allow_uri: bool=True,
                        max_method_length: int=10,
                        method_length_count_comments: bool=False,
                        max_parameters: int=5,
                        count_keyword_args: bool=True,
                        ignore_unused_block_args_if_empty: bool=True,
                        allow_unused_block_keyword_arguments: bool=False,
                        ignore_unused_method_args_if_empty: bool=True,
                        allow_unused_method_keyword_args: bool=False):
        """
        Not all settings added.
        Notable settings missing: Rails settings.

        :param access_modifier_indentation:
            Indent private/protected/public as deep as method definitions
            options:
                ``indent`` :  Indent modifiers like class members.
                ``outdent`` : Indent modifiers one level less than
                              class members.
        :param preferred_alias:
            Which method to use for aliasing in ruby.
            options : ``alias`` , ``alias_method``.
        :param align_hash_rocket_by:
            Alignment of entries using hash rocket as separator.
        :param align_colon_by:
            Alignment of entries using colon as separator.
        :param inspect_last_argument_hash:
            Select whether hashes that are the last argument in a method call
            should be inspected.
            options: ``always_inspect``, ``always_ignore``,
                     ``ignore_implicit``, ``ignore_explicit``.
        :param align_parameters:
            Alignment of parameters in multi-line method calls.

            options:
                ``with_first_parameter``: Aligns the following lines
                                          along the same column as the
                                          first parameter.

                ``with_fixed_indentation``: Aligns the following lines with one
                                            level of indentation relative to
                                            the start of the line with the
                                            method call.
        :param class_check:
            How to check type of class.
            options: ``is_a?``, ``kind_of?``.
        :param comment_keywords:
            Checks formatting of special comments based on keywords like
            TODO, FIXME etc.
        :param min_if_unless_guard:
            The number of lines that are tolerable within an if/unless block,
            more than these lines call for the usage of a guard clause.
        :param indent_size:
            Number of spaces per indentation level.
        :param method_naming_convention:
            Case of a method's name.
            options: ``snake``, ``camel``.
        :param string_literals:
            Use ' or " as string literals.
            options: ``single_quotes``, ``double_quotes``.
        :param variable_naming_convention:
            Case of a variable's name.
            options: ``snake``, ``camel``.
        :param max_class_length:
            Max lines in a class.
        :param class_length_count_comments:
            Whether or not to count comments while calculating the class
            length.
        :param max_module_length:
            Max lines in a module.
        :param module_length_count_comments:
            Whether or not to count comments while calculating
            the module length.
        :param cyclomatic_complexity:
            Cyclomatic Complexity of the file.
        :param max_line_length:
            Max length of a line.
        :param line_length_allow_here_doc:
            Allow here-doc lines to be more than the max line length.
        :param line_length_allow_uri:
            To make it possible to copy or click on URIs in the code,
            we allow ignore long lines containing a URI to be longer than max
            line length.
        :param max_method_length:
            Max number of lines in a method.
        :param method_length_count_comments:
            Whether or not to count full line comments while calculating
            method length.
        :param max_parameters:
            Max number of parameters in parameter list.
        :param count_keyword_args:
            Count keyword args while counting all arguments?
        :param ignore_unused_block_args_if_empty:
            Ignore unused block arguments if block is empty.
        :param allow_unused_block_keyword_arguments:
            Allow unused block keyword arguments.
        :param ignore_unused_method_args_if_empty:
            Allows unused method argument if method is empty.
        :param allow_unused_method_keyword_args:
            Allows unused keyword arguments in a method.
        """
        naming_convention = {'camel': 'camelCase', 'snake': 'snake_case'}
        options = {
            'Style/AccessModifierIndentation': {
                'EnforcedStyle': access_modifier_indentation
            },
            'Style/Alias': {
                'EnforcedStyle': preferred_alias
            },
            'Style/AlignHash': {
                'EnforcedHashRocketStyle': align_hash_rocket_by,
                'EnforcedColonStyle': align_colon_by,
                'EnforcedLastArgumentHashStyle': inspect_last_argument_hash
            },
            'Style/AlignParameters': {
                'EnforcedStyle': align_parameters
            },
            'Style/ClassCheck': {
                'EnforcedStyle': class_check
            },
            'Style/CommentAnnotation': {
                'Keywords': comment_keywords
            },
            'Style/GuardClause': {
                'MinBodyLength': min_if_unless_guard
            },
            'Style/IndentationWidth': {
                'Width': indent_size
            },
            'Style/MethodName': {
                'EnforcedStyle': naming_convention.get(
                                 method_naming_convention,
                                 method_naming_convention)
            },
            'Style/StringLiterals': {
                 'EnforcedStyle': string_literals
            },
            'Style/VariableName': {
                'EnforcedStyle': naming_convention.get(
                                 variable_naming_convention,
                                 variable_naming_convention)
            },
            'Metrics/ClassLength': {
                'Max': max_class_length,
                'CountComments': class_length_count_comments
            },
            'Metrics/ModuleLength': {
                'CountComments': module_length_count_comments,
                'Max': max_module_length
            },
            'Metrics/CyclomaticComplexity': {
                'Max': cyclomatic_complexity
            },
            'Metrics/LineLength': {
                'Max': max_line_length,
                'AllowHeredoc': line_length_allow_here_doc,
                'AllowURI': line_length_allow_uri
            },
            'Metrics/MethodLength': {
                'CountComments':  method_length_count_comments,
                'Max': max_method_length
            },
            'Metrics/ParameterLists': {
                'Max': max_parameters,
                'CountKeywordArgs': count_keyword_args
            },
            'Lint/UnusedBlockArgument': {
                'IgnoreEmptyBlocks': ignore_unused_block_args_if_empty,
                'AllowUnusedKeywordArguments':
                    allow_unused_block_keyword_arguments
            },
            'Lint/UnusedMethodArgument': {
                'AllowUnusedKeywordArguments':
                    allow_unused_method_keyword_args,
                'IgnoreEmptyMethods':
                    ignore_unused_method_args_if_empty
            },
        }
        return yaml.dump(options, default_flow_style=False)

    def process_output(self, output, filename, file):
        output = json.loads(output)
        assert len(output['files']) == 1
        for result in output['files'][0]['offenses']:
            # TODO: Add condition for auto-correct, when rubocop is updated.
            # Relevant Issue: https://github.com/bbatsov/rubocop/issues/2932
            yield Result.from_values(
                origin='{class_name} ({rule})'.format(
                    class_name=self.__class__.__name__,
                    rule=result['cop_name']),
                message=result['message'],
                file=filename,
                diffs=None,
                severity=self.severity_map[result['severity']],
                line=result['location']['line'],
                column=result['location']['column'],
                # Tested with linebreaks, it's secure.
                end_column=result['location']['column'] +
                result['location']['length'])
