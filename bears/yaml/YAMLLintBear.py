from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from dependency_management.requirements.PipRequirement import PipRequirement
import yaml


@linter(executable='yamllint',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+): '
                     r'\[(?P<severity>error|warning)\] (?P<message>.+)',
        severity_map={'error': RESULT_SEVERITY.MAJOR,
                      'warning': RESULT_SEVERITY.NORMAL})
class YAMLLintBear:
    """
    Check yaml code for errors and possible problems.

    You can read more about capabilities at
    <http://yamllint.readthedocs.org/en/latest/rules.html>.
    """

    LANGUAGES = {'YAML'}
    REQUIREMENTS = {PipRequirement('yamllint', '1.12.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting'}

    @staticmethod
    def generate_config(filename, file,
                        document_start: bool = None,
                        max_line_length: int = 80,
                        ):
        """
        :param document_start:
            Use this rule to require or forbid the use of document start
            marker (---).
        :param max_line_length:
            Maximum number of characters for a line, the newline character
            being excluded.
        """
        yamllint_configs = {
            'extends': 'default',
            'rules': {
                'document-start': 'disable' if document_start is None
                                  else {'present': document_start},
                'line-length': {
                    'max': max_line_length,
                    },
            },
        }

        return yaml.dump(yamllint_configs)

    @staticmethod
    def create_arguments(filename, file, config_file,
                         yamllint_config: str = '',
                         ):
        """
        :param yamllint_config: Path to a custom configuration file.
        """
        args = ('-f', 'parsable', filename)
        if yamllint_config:
            args += ('--config-file=' + yamllint_config,)
        else:
            args += ('--config-file=' + config_file,)
        return args
