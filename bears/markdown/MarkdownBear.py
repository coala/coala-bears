import json
import re

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.bearlib import deprecate_settings


@linter(executable='remark',
        use_stdin=True,
        use_stdout=True,
        use_stderr=True)
class MarkdownBear:
    """
    Check and correct Markdown style violations automatically.

    See <https://github.com/wooorm/remark-lint> for details about the tool
    below.
    """

    LANGUAGES = {'Markdown'}
    REQUIREMENTS = {NpmRequirement('remark-cli', '2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}

    _output_regex = re.compile(
        r'\s*(?P<line>\d+):(?P<column>\d+)'
        r'\s*(?P<severity>warning)\s*(?P<message>.*)')

    @staticmethod
    @deprecate_settings(bullets='markdown_bullets',
                        closed_headings='markdown_closed_headings',
                        setext_headings='markdown_setext_headings',
                        emphasis='markdown_emphasis',
                        strong='markdown_strong',
                        encode_entities='markdown_encode_entities',
                        codefence='markdown_codefence',
                        fences='markdown_fences',
                        list_indent='markdown_list_indent',
                        loose_tables='markdown_loose_tables',
                        spaced_tables='markdown_spaced_tables',
                        list_increment='markdown_list_increment',
                        horizontal_rule='markdown_horizontal_rule',
                        horizontal_rule_spaces='markdown_horizontal_'
                                               'rule_spaces',
                        horizontal_rule_repeat='markdown_horizontal_'
                                               'rule_repeat')
    def create_arguments(filename, file, config_file,
                         bullets: str='-',
                         closed_headings: bool=False,
                         setext_headings: bool=False,
                         emphasis: str='*',
                         strong: str='*',
                         encode_entities: bool=False,
                         codefence: str='`',
                         fences: bool=True,
                         list_indent: str='1',
                         loose_tables: bool=False,
                         spaced_tables: bool=True,
                         list_increment: bool=True,
                         horizontal_rule: str='*',
                         horizontal_rule_spaces: bool=False,
                         horizontal_rule_repeat: int=3,
                         max_line_length: int=80):
        """
        :param bullets:
            Character to use for bullets in lists. Can be "-", "*" or "+".
        :param closed_headings:
            Whether to close Atx headings or not. if true, extra # marks will
            be required after the heading. eg: `## Heading ##`.
        :param setext_headings:
            Whether to use setext headings. A setext heading uses underlines
            instead of # marks.
        :param emphasis:
            Character to wrap strong emphasis by. Can be "_" or "*".
        :param strong:
            Character to wrap slight emphasis by. Can be "_" or "*".
        :param encode_entities:
            Whether to encode symbols that are not ASCII into special HTML
            characters.
        :param codefence:
            Used to find which characters to use for code fences. Can be "`" or
            "~".
        :param fences:
            Use fences for code blocks.
        :param list_indent:
            Used to find spacing after bullet in lists. Can be "1", "tab" or
            "mixed".
            - "1" - 1 space after bullet.
            - "tab" - Use tab stops to begin a sentence after the bullet.
            - "mixed" - Use "1" when the list item is only 1 line, "tab" if it
              spans multiple.
        :param loose_tables:
            Whether to use pipes for the outermost borders in a table.
        :param spaced_tables:
            Whether to add space between pipes in a table.
        :param list_increment:
            Whether an ordered lists numbers should be incremented.
        :param markdown_horizontal_rule:
            The horizontal rule character. Can be '*', '_' or '-'.
        :param horizontal_rule_spaces:
            Whether spaces should be added between horizontal rule characters.
        :param horizontal_rule_repeat:
            The number of times the horizontal rule character will be repeated.
        :param max_line_length:
            The maximum line length allowed.
        """
        remark_configs_settings = {
            'bullet': bullets,                          # - or *
            'closeAtx': closed_headings,                # Bool
            'setext': setext_headings,                  # Bool
            'emphasis': emphasis,                       # char (_ or *)
            'strong': strong,                           # char (_ or *)
            'entities': encode_entities,                # Bool
            'fence': codefence,                         # char (~ or `)
            'fences': fences,                           # Bool
            'listItemIndent': list_indent,              # int or "tab"
                                                        # or "mixed"
            'looseTable': loose_tables,                 # Bool
            'spacedTable': spaced_tables,               # Bool
            'incrementListMarker': list_increment,      # Bool
            'rule': horizontal_rule,                    # - or * or _
            'ruleSpaces': horizontal_rule_spaces,       # Bool
            'ruleRepetition': horizontal_rule_repeat,   # int
        }
        remark_configs_plugins = {
            'maximumLineLength': max_line_length        # int
        }

        config_json = json.dumps(remark_configs_settings)
        # Remove { and } as remark adds them on its own
        settings = config_json[1:-1]
        config_json = json.dumps(remark_configs_plugins)
        plugins = 'lint=' + config_json[1:-1]
        return '--no-color', '--quiet', '--setting', settings, '--use', plugins

    def process_output(self, output, filename, file):
        stdout, stderr = output
        yield from self.process_output_corrected(stdout, filename, file,
                                                 RESULT_SEVERITY.NORMAL,
                                                 'The text does not comply'
                                                 ' to the set style.')
        yield from self.process_output_regex(stderr, filename, file,
                                             self._output_regex)
