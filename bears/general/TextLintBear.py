import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import typed_list
from dependency_management.requirements.NpmRequirement import NpmRequirement
from dependency_management.requirements.PipRequirement import PipRequirement


@linter(executable='textlint',
        output_format='regex',
        output_regex=r'(?P<line>\d+):(?P<column>\d+)(?:\s|\u2713)*'
                     r'(?P<severity>error|warning)\s+(?P<message>.+?)'
                     r'(?:  .*|\n|$)')
class TextLintBear:
    """
    The pluggable linting tool for text and Markdown. It is similar to ESLint,
    but covers natural language instead.
    """

    LANGUAGES = {'HTML', 'Markdown', 'reStructuredText'}
    REQUIREMENTS = {NpmRequirement('textlint', '7.3.0'),
                    NpmRequirement('textlint-plugin-asciidoctor', '1.0.3'),
                    NpmRequirement('textlint-plugin-html', '0.1.5'),
                    NpmRequirement('textlint-plugin-review', '0.3.3'),
                    NpmRequirement('textlint-plugin-rst', '0.1.1'),
                    NpmRequirement('textlint-rule-alex', '1.2.0'),
                    NpmRequirement('textlint-rule-common-misspellings',
                                   '1.0.1'),
                    NpmRequirement('textlint-rule-date-weekday-mismatch',
                                   '1.0.5'),
                    NpmRequirement('textlint-rule-ginger', '>=2.1.0 <2.1.2'),
                    NpmRequirement('textlint-rule-max-comma', '1.0.4'),
                    NpmRequirement('textlint-rule-max-number-of-lines',
                                   '1.0.3'),
                    NpmRequirement('textlint-rule-ng-word', '1.0.0'),
                    NpmRequirement('textlint-rule-no-dead-link', '3.1.1'),
                    NpmRequirement('textlint-rule-no-empty-section', '1.1.0'),
                    NpmRequirement('textlint-rule-no-start-'
                                   'duplicated-conjunction', '1.1.3'),
                    NpmRequirement('textlint-rule-no-todo', '2.0.0'),
                    NpmRequirement('textlint-rule-period-in-list-item',
                                   '0.2.0'),
                    NpmRequirement('textlint-rule-rousseau', '1.4.5'),
                    NpmRequirement('textlint-rule-unexpanded-acronym',
                                   '1.2.1'),
                    NpmRequirement('textlint-rule-write-good', '1.6.0'),
                    # Dependency for textlint-plugin-rst
                    PipRequirement('docutils-ast-writer', '0.1.2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Grammar', 'Spelling'}
    SEE_MORE = 'https://github.com/textlint/textlint'

    @staticmethod
    def generate_config(filename, file,
                        check_todos: bool = None,
                        dont_start_with_duplicated_conjunction: bool = True,
                        no_empty_section: bool = True,
                        check_date_weekday_mismatch: bool = True,
                        check_grammar: bool = True,
                        max_lines_per_file: int = 300,
                        max_comma_per_sentence: int = 4,
                        no_good_words: typed_list(str) = [],
                        period_in_list_item: bool = True,
                        minimum_acronym_length: int = 3,
                        maximum_acronym_length: int = 5,
                        ignore_acronyms: typed_list(str) = [],
                        check_with_rousseau: bool = True,
                        check_with_alex: bool = True,
                        check_common_misspellings: bool = True,
                        allow_passive_voice: bool = True,
                        allow_so_beginning: bool = True,
                        allow_adverbs: bool = True,
                        allow_repeated_words: bool = True,
                        allow_there_is: bool = True,
                        allow_ambiguous_words: bool = True,
                        allow_extra_words: bool = True,
                        allow_cliche_phrases: bool = True,
                        check_relative_links: bool = False,
                        base_uri: str = '',
                        link_ignore_list: typed_list(str) = [],
                        textlint_config: str = '',
                        ):
        """
        :param check_todos:
            This rule checks for occurrences of ``- [ ]``
            (so called task lists).
        :param dont_start_with_duplicated_conjunction:
            This rule checks whether your sentence starts with a duplicated
            conjunction.
        :param no_empty_section:
            This rule does not allow to create an empty section.
            For example, there is an empty section ``# Header A`` below::

                # Header A

                # Header B
                Text.

        :param check_date_weekday_mismatch:
            This rule finds a mismatch between a date and the corresponding
            weekday.
        :param check_grammar:
            This rule checks your English grammar with Ginger Proofreading.
        :param max_lines_per_file:
            Number of lines allowed per file.
        :param max_comma_per_sentence:
            Number of commas allowed per sentence.
        :param no_good_words:
            Set of NG (No Good) words to check for.
        :param period_in_list_item:
            Checks whether a sentence in a list item ends with a period.
        :param minimum_acronym_length:
            Minimum length for unexpanded acronyms.
        :param maximum_acronym_length:
            Maximum length for unexpanded acronyms.
        :param ignore_acronyms:
            A list that contains the acronyms to ignore.
        :param check_with_rousseau:
            This rule checks English writing using Rousseau, which is a
            lightweight proofreader written in JavaScript.
            It can check:
            - Passive voice
            - Lexical illusions – cases where a word is repeated
            - 'So' at the beginning of the sentence
            - Adverbs that can weaken meaning: really, very, extremely, etc.
            - Readability of sentences
            - Simpler expressions
            - Weasel words
            - If a sentence is preceded by a space
            - If there is no space between a sentence and its ending
              punctuation
            - If sentences are starting with uppercase letter
        :param check_with_alex:
            This rule helps you find gender favouring, polarising, race
            related, religion inconsiderate, or other unequal phrasing
            and checks for:
            - Gendered work-titles, for example warning about ``garbageman``
              and suggesting ``garbage collector`` instead
            - Gendered proverbs, such as warning about ``like a man`` and
              suggesting ``bravely`` instead, or warning about ``ladylike``
              and suggesting ``courteous``
            - Blunt phrases, such as warning about ``cripple`` and suggesting
              ``person with a limp`` instead
            - Intolerant phrasing, such as warning about using ``master`` and
              ``slave`` together, and suggesting ``primary`` and ``replica``
              instead
        :param check_common_misspellings:
            This rule helps to find common misspellings from Wikipedia's
            list of common misspellings.
        :param allow_passive_voice:
            Allows passive voice.
        :param allow_so_beginning:
            Allows ``So`` at the beginning of a sentence.
        :param allow_adverbs:
            Allows adverbs that can weaken the meaning, such as: ``really``,
            ``very``, ``extremely``, etc.
        :param allow_repeated_words:
            Allows lexical illusions, i.e. cases where a word is repeated.
        :param allow_there_is:
            Allows ``There is`` or ``There are`` at the beginning of a
            sentence.
        :param allow_ambiguous_words:
            Allows "weasel words", for example "often" or "probably".
        :param allow_extra_words:
            Allows wordy phrases and unnecessary words.
        :param allow_cliche_phrases:
            Allows common cliche phrases in the sentence.
            For example: In the sentence
            "Writing specs puts me at loose ends.",
            "at loose ends" is a cliche.
        :param check_relative_links:
            This rule enables dead link checks against relative URIs.
            Note that you also have to specify the ``base_uri`` to make this
            option work.
        :param base_uri:
            The base URI to be used for resolving relative URIs.
        :param link_ignore_list:
            A list of URIs to be ignored, i.e. skipped from availability
            checks.
        """
        if textlint_config:
            return None
        else:
            options = {
                'no-todo': check_todos,
                'no-start-duplicated-conjunction':
                    dont_start_with_duplicated_conjunction,
                'no-empty-section': no_empty_section,
                'date-weekday-mismatch': check_date_weekday_mismatch,
                'ginger': check_grammar,
                'max-number-of-lines': {
                    'max': max_lines_per_file
                },
                'max-comma': {
                    'max': max_comma_per_sentence
                },
                'ng-word': {
                    'words': no_good_words
                },
                'period-in-list-item': period_in_list_item,
                'unexpanded-acronym': {
                    'min_acronym_len': minimum_acronym_length,
                    'max_acronym_len': maximum_acronym_length,
                    'ignore_acronyms': ignore_acronyms
                },
                'rousseau': check_with_rousseau,
                'alex': check_with_alex,
                'common-misspellings': check_common_misspellings,
                'write-good': {
                    'passive': allow_passive_voice,
                    'so': allow_so_beginning,
                    'adverb': allow_adverbs,
                    'illusion': allow_repeated_words,
                    'thereIs': allow_there_is,
                    'weasel': allow_ambiguous_words,
                    'tooWordy': allow_extra_words,
                    'cliches': allow_cliche_phrases
                },
                'no-dead-link': {
                    'checkRelative': check_relative_links,
                    'baseURI': base_uri,
                    'ignore': link_ignore_list
                }
            }

            parent_config = {
                'rules': options,
                'plugins': ['asciidoctor', 'html', 'review', 'rst']
            }

            return json.dumps(parent_config)

    @staticmethod
    def create_arguments(filename, file, config_file,
                         textlint_config: str = '',
                         ):
        """
        :param textlint_config:
            The location of the ``.textlintrc`` config file.
        """
        return ('-c',
                textlint_config if textlint_config else config_file,
                filename)
