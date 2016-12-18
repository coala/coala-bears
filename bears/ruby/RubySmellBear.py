import json

from coalib.bearlib import deprecate_settings
from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GemRequirement import GemRequirement
from coalib.results.Result import Result
from coalib.results.SourceRange import SourceRange
from coala_utils.param_conversion import negate


@linter(executable='reek', use_stdin=True)
class RubySmellBear:
    """
    Detect code smells in Ruby source code.

    For more information about the detected smells, see
    <https://github.com/troessner/reek/blob/master/docs/Code-Smells.md>.
    """

    LANGUAGES = {'Ruby'}
    REQUIREMENTS = {GemRequirement('reek')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Smell'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--format', 'json', '-c', config_file

    def process_output(self, output, filename, file):
        output = json.loads(output) if output else ()
        for issue in output:
            sourceranges = []
            for line in issue['lines']:
                sourceranges.append(SourceRange.from_values(
                    file=filename, start_line=line))

            if 'name' in issue:
                message = "'{}' (in '{}') {}.".format(
                    issue['name'], issue['context'], issue['message'])
            else:
                message = "'{}' {}".format(issue['context'], issue['message'])

            yield Result(
                origin='{} ({})'.format(self.__class__.__name__,
                                        issue['smell_type']),
                message=message,
                affected_code=sourceranges,
                additional_info='More information is available at {}'
                                '.'.format(issue['wiki_link']))

    @deprecate_settings(allow_duplicate_method=(
                            'duplicate_method_call', negate),
                        allow_data_clump=('data_clump', negate),
                        allow_control_parameters=('control_parameter', negate),
                        allow_class_variables=('class_variable', negate),
                        allow_boolean_parameter_in_functions=(
                            'boolean_parameter', negate),
                        allow_setter_in_classes=('attribute', negate),
                        allow_unused_private_methods=(
                            'unused_private_method', negate),
                        allow_unused_variables=('unused_params', negate))
    def generate_config(self,
                        allow_setter_in_classes: bool=False,
                        allow_boolean_parameter_in_functions: bool=False,
                        allow_class_variables: bool=False,
                        allow_control_parameters: bool=False,
                        allow_data_clump: bool=False,
                        allow_duplicate_method: bool=False,
                        feature_envy: bool=True,
                        missing_module_description: bool=True,
                        long_param_list: bool=True,
                        long_yield_list: bool=True,
                        module_initialize: bool=True,
                        nested_iterators: bool=True,
                        nil_check: bool=True,
                        prima_donna_method: bool=True,
                        repeated_conditional: bool=True,
                        too_many_instance_variables: bool=True,
                        too_many_methods: bool=True,
                        too_long_method: bool=True,
                        bad_method_name: bool=True,
                        bad_module_name: bool=True,
                        bad_param_name: bool=True,
                        bad_var_name: bool=True,
                        allow_unused_variables: bool=False,
                        allow_unused_private_methods: bool=True,
                        utility_function: bool=True):
        """
        :param allow_setter_in_classes:
            Allows setter in classes.
        :param allow_boolean_parameter_in_functions:
            Allows boolean parameter in functions (control coupling).
        :param allow_class_variables:
            Allows class variables.
        :param allow_control_parameters:
            Allows parameters that control function behaviour (control
            coupling).
        :param allow_data_clump:
            Does not warn when the same two or three items frequently appear
            together in function/class parameter list.
        :param allow_duplicate_method:
            Allows having two fragments of code that look nearly identical, or
            two fragments of code that have nearly identical effects at some
            conceptual level.
        :param feature_envy:
            Occurs when a code fragment references another object more often
            than it references itself, or when several clients do the same
            series of manipulations on a particular type of object.
        :param missing_module_description:
            Warns if a module description is missing.
        :param long_param_list:
            Warns about too many parameters of functions.
        :param long_yield_list:
            Warns when a method yields a lot of arguments to the block it gets
            passed.
        :param module_initialize:
            Warns about ``#initialize`` methods in modules.
        :param nested_iterators:
            Warns when a block contains another block.
        :param nil_check:
            Warns about nil checks.
        :param prima_donna_method:
            Warns about methods whose names end with an exclamation mark.
        :param repeated_conditional:
            Warns about repeated conditionals.
        :param too_many_instance_variables:
            Warns for too many instance variables.
        :param too_many_methods:
            Warns if a class has too many methods.
        :param too_long_method:
            Warns about huge methods.
        :param bad_method_name:
            Warns about method names which are not communicating the purpose
            of the method well.
        :param bad_module_name:
            Warns about module names which are not communicating the purpose
            of the module well.
        :param bad_param_name:
            Warns about parameter names which are not communicating the purpose
            of the parameter well.
        :param bad_var_name:
            Warns about variable names which are not communicating the purpose
            of the variable well.
        :param allow_unused_variables:
            Allows unused parameters though they are dead code.
        :param check_unused_private_methods:
            Warns about unused private methods, as they are dead code.
        :param utility_function:
            Allows any instance method that has no dependency on the state of
            the instance.
        """
        config = {
            'Attribute': not allow_setter_in_classes,
            'BooleanParameter': not allow_boolean_parameter_in_functions,
            'ClassVariable': not allow_class_variables,
            'ControlParameter': not allow_control_parameters,
            'DataClump': not allow_data_clump,
            'DuplicateMethodCall': not allow_duplicate_method,
            'FeatureEnvy': feature_envy,
            'IrresponsibleModule': missing_module_description,
            'LongParameterList': long_param_list,
            'LongYieldList': long_yield_list,
            'ModuleInitialize': module_initialize,
            'NestedIterators': nested_iterators,
            'NilCheck': nil_check,
            'PrimaDonnaMethod': prima_donna_method,
            'RepeatedConditional': repeated_conditional,
            'TooManyInstanceVariables': too_many_instance_variables,
            'TooManyMethods': too_many_methods,
            'TooManyStatements': too_long_method,
            'UncommunicativeMethodName': bad_method_name,
            'UncommunicativeModuleName': bad_module_name,
            'UncommunicativeParameterName': bad_param_name,
            'UncommunicativeVariableName': bad_var_name,
            'UnusedParameters': not allow_unused_variables,
            'UnusedPrivateMethod': not allow_unused_private_methods,
            'UtilityFunction': utility_function}

        return ('---\n' +
                '\n'.join('{}:\n  enabled: {}'.format(key, str(value).lower())
                          for key, value in config.items()))
