import json
from typing import List, Union

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(executable='rehype',
        output_format='corrected',
        use_stdin=True)
class HTMLFormatBear:
    """
    Formats HTML automatically using rehype-format.
    """
    LANGUAGES = {'HTML'}
    REQUIREMENTS = {NpmRequirement('rehype-cli', '7.0.0'),
                    NpmRequirement('rehype-format', '2.3.1'),
                    }
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}
    SEE_MORE = 'https://github.com/wooorm/rehype-format'

    def generate_config(filename, file,
                        indent: Union[str, int] = 2,
                        indent_initial: bool = True,
                        blanks: List[str] = []):
        """
        :param indent:
            Indentation per level. When number, uses that amount of spaces. When
            string, uses that per indentation level.
        :param indent_initial:
            Whether to indent the first level.
        :param blanks:
            List of tag-names, which, when next to each other, are joined by a
            blank line (\n\n).
        """
        rehype_format_configs = {
            'config': ['format'],
            'indent': indent,
            'indentInitial': indent_initial,
            'blanks': blanks,
        }
        return json.dumps(rehype_format_configs)

    @staticmethod
    def create_arguments(filename, file, config_file):
        return (filename, '--quiet', '--no-color', '--use', 'format',
                '--output', '--rc-path', config_file)
