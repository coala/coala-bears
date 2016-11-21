import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.NpmRequirement import NpmRequirement
from coalib.results.Result import Result
from coalib.settings.Setting import path
from coalib.misc.ContextManagers import prepare_file


@linter(executable='tslint',
        config_suffix='.json')
class TSLintBear:
    """
    Check TypeScript code for style violations and possible semantical
    problems.

    Read more about the capabilities at
    <https://github.com/palantir/tslint#core-rules>.
    """

    LANGUAGES = {"TypeScript"}
    REQUIREMENTS = {NpmRequirement('tslint', '3.9'),
                    NpmRequirement('codelyzer', '0.0.28')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/9re9c4fv17lhn7rmvzueebb3b'
    CAN_DETECT = {'Syntax', 'Formatting', 'Smell'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         tslint_config: path="",
                         rules_dir: path=""):
        """
        :param tslint_config:
            Path to configuration file. This will override all the settings
            provided here.
        :param rules_dir:
            An additional rules directory, for user-created rules.
        """
        args = ('--format', 'json', '--config')
        args += (tslint_config,) if tslint_config else (config_file,)
        if rules_dir:
            args += ('--rules-dir', rules_dir)
        return args + (filename,)

    @staticmethod
    def generate_config(filename, file,
                        directive_selectors_naming_convention: str="camel",
                        component_selectors_naming_convention: str="hyphen",
                        check_directive_selectors_type: bool=True,
                        directive_selectors_type: str="attribute",
                        check_component_selectors_type: bool=True,
                        component_selectors_type: str="element",
                        force_directive_selectors_prefix: bool=True,
                        directive_selectors_prefix: str="sg",
                        force_component_selectors_prefix: bool=True,
                        component_selectors_prefix: str="sg",
                        use_input_property_decorators: bool=True,
                        use_output_property_decorators: bool=True,
                        use_host_property_decorators: bool=True,
                        allow_attribute_parameter_decorators: bool=False,
                        allow_input_rename: bool=False,
                        allow_output_rename: bool=False,
                        allow_forward_references: bool=False,
                        use_life_cycle_interface: bool=True,
                        use_pipe_transform_interface: bool=True,
                        pipe_naming_convention: str="camel",
                        pipe_prefix: str="sg",
                        force_pipe_prefix: bool=True,
                        component_class_suffix: bool=True,
                        directive_class_suffix: bool=True,
                        check_import_destructuring_spacing: bool=True):
        """
        :param tslint_config:
            Path to configuration file. This will override all the settings
            provided here.
        :param rules_dir:
            An additional rules directory, for user-created rules.
        :param directive_selectors_naming_convention:
            Naming convention to use for directives selectors (``hyphen``,
            ``camel`` (default), ``snake``).
        :param component_selectors_naming_convention:
            Naming convention to use for components' selectors (``hyphen``
            (default), ``camel``, ``snake``).
        :param check_directive_selectors_type:
            Checks for the type of directives.
        :param directive_selectors_type:
            Use directives either as ``element`` or ``attribute`` (default).
        :param check_component_selectors_type:
            Checks for the type of components.
        :param component_selectors_type:
            Use components either as ``element`` (default) or ``attribute``.
        :param force_directive_selectors_prefix:
            Enforces the use of a custom prefix for directives.
        :param directive_selectors_prefix:
            Use a custom prefix for the selector of our directives, to prevent
            name collision.
        :param force_component_selectors_prefix:
            Enforces the use of a custom prefix for components.
        :param component_selectors_prefix:
            Use a custom prefix for the selector of our components.
        :param use_input_property_decorators:
            Use ``@Input`` instead of the input properties of the
            ``@Directive`` and ``@Component`` decorators.
        :param use_output_property_decorators:
            Use ``@output`` instead of the output properties of the
            ``@Directive`` and ``@Component`` decorators.
        :param use_host_property_decorators:
            Use ``@HostListener`` and ``@HostBinding`` instead of the host
            property of the ``@Directive`` and ``@Component`` decorators.
        :param allow_attribute_parameter_decorators:
            Allows using ``attribute`` decorator.
        :param allow_input_rename:
            Allows renaming directives input properties.
        :param allow_output_rename:
            Allows renaming directives output properties.
        :param allow_forward_references:
            Allows the use of ``forwardRef``.
            Example:
            ::
                @Component({
                  directives: [forwardRef(()=>NameService)]
                })
                class Test {}
                class NameService {}
        :param use_life_cycle_interface:
            Use life cycle hooks with their corresponding interfaces.
        :param pipe_naming_convention:
            Naming convention for pipes (``hyphen``, ``camel`` (default),
            ``snake``).
        :param pipe_prefix:
            Use a custom prefix for our pipe.
        :param force_pipe_prefix:
            Enforces the use of a custom prefix for pipes.
        :param component_class_suffix:
            Use ``Component`` as component classes name's suffix when
            the ``@Component`` decorator is used, ``Pipe`` when the ``@Pipe``
            decorator is used, and ``Empty`` when the class is empty.
        :param directive_class_suffix:
            Use ``Directive`` as directive classes name's suffix when
            the ``@Directive`` decorator is used, ``Pipe`` when the ``@Pipe``
            decorator is used, and ``Empty`` when the class is empty.
            is used and ``Empty`` when the class is empty.
        :param check_import_destructuring_spacing:
            Checks valid spacing inside ``import`` statements.

        """
        naming_convention_map = {
            'camel': 'camelCase',
            'snake': 'snake_case',
            'hyphen': 'kebab-case'
        }
        _tslint_directive_selector_naming_convention = (
            naming_convention_map.get(
                directive_selectors_naming_convention, ''))
        _tslint_component_selector_naming_convention = (
            naming_convention_map.get(
               component_selectors_naming_convention, ''))
        rules = {
                 "directive-selector-name": [
                    _tslint_directive_selector_naming_convention is not '',
                    _tslint_directive_selector_naming_convention],
                 "component-selector-name": [
                    _tslint_component_selector_naming_convention is not '',
                    _tslint_component_selector_naming_convention],
                 "directive-selector-type":
                    [check_directive_selectors_type,
                     directive_selectors_type],
                 "component-selector-type":
                    [check_component_selectors_type,
                     component_selectors_type],
                 "directive-selector-prefix":
                    [force_directive_selectors_prefix,
                     directive_selectors_prefix],
                 "component-selector-prefix":
                    [force_component_selectors_prefix,
                     component_selectors_prefix],
                 "use-input-property-decorator":
                     use_input_property_decorators,
                 "use-output-property-decorator":
                     use_output_property_decorators,
                 "use-host-property-decorator":
                     use_host_property_decorators,
                 "no-attribute-parameter-decorator":
                     allow_attribute_parameter_decorators,
                 "no-input-rename": allow_input_rename,
                 "no-output-rename": allow_output_rename,
                 "no-forward-ref": allow_forward_references,
                 "use-life-cycle-interface": use_life_cycle_interface,
                 "use-pipe-transform-interface":
                     use_pipe_transform_interface,
                 "pipe-naming":
                    [force_pipe_prefix, pipe_naming_convention,
                     pipe_prefix],
                 "component-class-suffix": component_class_suffix,
                 "directive-class-suffix": directive_class_suffix,
                 "import-destructuring-spacing":
                     check_import_destructuring_spacing
                }
        configs = {"rulesDirectory": "node_modules/codelyzer",
                   "rules": rules}
        return json.dumps(configs)

    def process_output(self, output, filename, file):
        output = json.loads(output) if output else []
        for issue in output:
            yield Result.from_values(
                origin="{} ({})".format(self.__class__.__name__,
                                        issue['ruleName']),
                message=issue["failure"],
                file=issue["name"],
                line=int(issue["startPosition"]["line"]) + 1,
                end_line=int(issue["endPosition"]["line"]) + 1,
                column=int(issue["startPosition"]["character"]) + 1,
                end_column=int(issue["endPosition"]["character"]) + 1)
