import json
import re

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.bearlib import deprecate_settings


@linter(executable='remark',
        use_stdout=True,
        use_stderr=True)
class MarkdownBear:
    """
    Check and correct Markdown style violations automatically.

    See <https://github.com/wooorm/remark-lint> for details about the tool
    below.
    """

    LANGUAGES = {'Markdown'}
    REQUIREMENTS = {NpmRequirement('remark-cli', '2'),
                    NpmRequirement('remark-lint', '5'),
                    NpmRequirement('remark-validate-links', '5')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}

    _output_regex = re.compile(
        r'\s*(?P<line>\d+):(?P<column>\d+)'
        r'\s*(?P<severity>warning)\s*(?P<message>.+?)(?:  .*|\n|$)')

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
                         bullets: str = '-',
                         closed_headings: bool = False,
                         setext_headings: bool = False,
                         emphasis: str = '*',
                         strong: str = '*',
                         encode_entities: bool = False,
                         codefence: str = '`',
                         fences: bool = True,
                         list_indent: str = '1',
                         loose_tables: bool = False,
                         spaced_tables: bool = True,
                         list_increment: bool = True,
                         horizontal_rule: str = '*',
                         horizontal_rule_spaces: bool = False,
                         horizontal_rule_repeat: int = 3,
                         max_line_length: int = None,
                         check_links: bool = False,
                         blockquote_indentation: int = 2,
                         enforce_checkbox_content_indentation: bool = True,
                         code_block_style: str = 'consistent',
                         enforce_labels_at_eof: bool = True,
                         first_heading_level: int = None,
                         enforce_heading_level_increment: bool = False,
                         max_heading_length: int = 60,
                         prohibit_duplicate_definitions: bool = True,
                         prohibit_duplicate_headings_in_section: bool = True,
                         prohibit_duplicate_headings: bool = True,
                         prohibit_empty_url: bool = True,
                         prohibit_irregular_chars_filename:
                             str = '\\.a-zA-Z0-9-_',
                         prohibit_punctuations_in_heading: str = '.,;:!?',
                         prohibit_html: bool = True,
                         prohibit_shortcut_reference_image: bool = True,
                         prohibit_shortcut_reference_link: bool = True,
                         use_spaces: bool = True,
                         check_undefined_references: bool = True,
                         check_unused_definition: bool = True,
                         ):
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
        :param horizontal_rule:
            The horizontal rule character. Can be '*', '_' or '-'.
        :param horizontal_rule_spaces:
            Whether spaces should be added between horizontal rule characters.
        :param horizontal_rule_repeat:
            The number of times the horizontal rule character will be repeated.
        :param max_line_length:
            The maximum line length allowed.
        :param check_links:
            Checks if links to headings and files in markdown are valid.
        :param blockquote_indentation:
            Warn when blockquotes are either indented too much or too little.
        :param enforce_checkbox_content_indentation:
            Warn when list item checkboxes are followed by unnecessary
            whitespace.
        :param code_block_style:
            Warn when code-blocks do not adhere to a given style. Can be
            ``consistent``, ``fenced``, or ``indented``. The default value,
            ``consistent``, detects the first used code-block style, and will
            warn when a subsequent code-block uses a different style.
        :param enforce_labels_at_eof:
            Warn when definitions are not placed at the end of the file.
            For example: If set to ``True``, this will throw a warning::

                Paragraph.
                [example]: http://example.com "Example Domain"
                Another paragraph.

        :param first_heading_level:
            Warn when the first heading has a level other than a specified
            value.
            For example: If set to ``2``, this will throw a warning::

                # Bravo
                Paragraph.

        :param enforce_heading_level_increment:
            Warn when headings increment with more than 1 level at a time.
            For example: If set to ``True``, prefer this::

                # Alpha
                ## Bravo

            over this::

                # Alpha
                ### Bravo

        :param max_heading_length:
            The maximum heading length allowed. Ignores markdown syntax, only
            checks the plain text content.
        :param prohibit_duplicate_definitions:
            Warn when duplicate definitions are found.
            For example: If set to ``True``, this will throw a warning::

                [foo]: bar
                [foo]: qux

        :param prohibit_duplicate_headings_in_section:
            Warn when duplicate headings are found, but only when on the same
            level, “in” the same section.
            For example: If set to ``True``, this will throw a warning::

                ## Foxtrot
                ### Golf
                ### Golf

        :param prohibit_duplicate_headings:
            Warn when duplicate headings are found.
            For example: If set to ``True``, this will throw a warning::

                # Foo
                ## Foo
                ## [Foo](http://foo.com/bar)

        :param prohibit_empty_url:
            Warn for empty URLs in links and images.
            For example: If set to ``True``, this will throw a warning::

                [golf]().
                ![hotel]().

        :param prohibit_irregular_chars_filename:
            Warn when file names contain irregular characters: characters other
             than alpha-numericals, dashes, dots (full-stops) and underscores.
             Can take ``RegExp`` or ``string``. Any match by the given
             expression triggers a warning.
        :param prohibit_punctuations_in_heading:
            Warn when a heading ends with a group of characters. Can take a
            ``string`` that contains the group of characters.
        :param prohibit_html:
            Warn when HTML elements are used. Ignores comments, because they
            are used remark, because markdown doesn’t have native comments.
            For example: If set to ``True``, this will throw a warning::

                <h1>Hello</h1>

        :param prohibit_shortcut_reference_image:
            Warn when shortcut reference images are used.
            For example: If set to ``True``, this will throw a warning::

                ![foo]
                [foo]: http://foo.bar/baz.png

        :param prohibit_shortcut_reference_link:
            Warn when shortcut reference links are used.
            For example: If set to ``True``, this will throw a warning::

                [foo]
                [foo]: http://foo.bar/baz

        :param use_spaces:
            Warn when tabs are used instead of spaces.
        :param check_undefined_references:
            Warn when references to undefined definitions are found.
            For example: If set to ``True``, this will throw a warning::

                [bar][]

        :param check_unused_definition:
            Warn when unused definitions are found.
            For example: If set to ``True``, this will throw a warning::

                [bar]: https://example.com

        """
        remark_configs = {
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
        remark_lint_configs = {
            'blockquoteIndentation': blockquote_indentation,
            'checkboxContentIndent': enforce_checkbox_content_indentation,
            'codeBlockStyle': code_block_style,
            'finalDefinition': enforce_labels_at_eof,
            'firstHeadingLevel': first_heading_level,
            'headingIncrement': enforce_heading_level_increment,
            'maximumHeadingLength': max_heading_length,
            'noDuplicateDefinitions': prohibit_duplicate_definitions,
            'noDuplicateHeadingsInSection':
                prohibit_duplicate_headings_in_section,
            'noDuplicateHeadings': prohibit_duplicate_headings,
            'noEmptyURL': prohibit_empty_url,
            'noFileNameIrregularCharacters': prohibit_irregular_chars_filename,
            'noHeadingPunctuation': prohibit_punctuations_in_heading,
            'noHTML': prohibit_html,
            'noShortcutReferenceImage': prohibit_shortcut_reference_image,
            'noShortcutReferenceLink': prohibit_shortcut_reference_link,
            'noTabs': use_spaces,
            'noUndefinedReferences': check_undefined_references,
            'noUnusedDefinitions': check_unused_definition,
        }

        if max_line_length:
            remark_lint_configs['maximumLineLength'] = max_line_length

        config_json = json.dumps(remark_configs)
        # Remove { and } as remark adds them on its own
        settings = config_json[1:-1]

        args = [filename, '--no-color', '--quiet', '--setting', settings]

        config_json = json.dumps(remark_lint_configs)
        lint = 'lint=' + config_json[1:-1]
        args += ['--use', lint]

        if check_links:
            args += ['--use', 'validate-links']

        return args

    def process_output(self, output, filename, file):
        stdout, stderr = output
        yield from self.process_output_corrected(stdout, filename, file,
                                                 RESULT_SEVERITY.NORMAL,
                                                 'The text does not comply'
                                                 ' to the set style.')
        yield from self.process_output_regex(stderr, filename, file,
                                             self._output_regex)
