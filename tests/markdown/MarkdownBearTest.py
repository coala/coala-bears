import unittest
from queue import Queue

from bears.markdown.MarkdownBear import MarkdownBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import verify_local_bear, execute_bear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coala_utils.ContextManagers import prepare_file


test_file1 = """1. abc
1. def
"""


test_file2 = """1. abc
2. def
"""

test_file3 = """1. abcdefghijklm
2. nopqrstuvwxyz
"""

test_file4 = """# Hello

Read more [This link does not exist](#world).
"""

test_file5 = """# world

Read more [This link exists](#world).
"""

blockquote_indentation_file = """>  Hello

Paragraph.
"""

checkbox_content_indentation_file = """Some line.

- [x]  List item
"""

labels_at_eof_unused_definition_file = """Paragraph.

[example]: http://example.com "Example Domain"

Another paragraph.
"""

first_heading_level_file = """# Bravo

Paragraph.
"""

heading_level_increment_file = """# Charlie

### Delta
"""

empty_url_file = """[golf](<>).

![hotel](<>).
"""

duplicate_heading_file = """## Foxtrot

### Golf

### Golf
"""

punctuation_in_heading_file = """# Hello:

# Hello?

# Hello!
"""

html_file = """<h1>Hello</h1>
"""

MarkdownBearTest = verify_local_bear(MarkdownBear,
                                     valid_files=(test_file2,),
                                     invalid_files=(test_file1,))

MarkdownBearConfigsTest = verify_local_bear(
    MarkdownBear,
    valid_files=(test_file1,),
    invalid_files=(test_file2,),
    settings={'list_increment': False})

MarkdownBearMaxLineLengthSettingTest = verify_local_bear(
    MarkdownBear,
    valid_files=(test_file2,),
    invalid_files=(test_file3,),
    settings={'max_line_length': 10})


@generate_skip_decorator(MarkdownBear)
class MarkdownBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('name')
        self.uut = MarkdownBear(self.section, Queue())

    def test_invalid_message(self):
        content = test_file3.splitlines()
        self.section.append(Setting('max_line_length', '10'))
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].message,
                                 'Line must be at most 10 characters')
                self.assertEqual(results[0].severity, RESULT_SEVERITY.NORMAL)

    def test_invalid_link(self):
        content = test_file4.splitlines()
        self.section.append(Setting('check_links', True))
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].message,
                                 'Link to unknown heading: `world`')
                self.assertEqual(results[0].severity, RESULT_SEVERITY.NORMAL)

    def test_valid_link(self):
        content = test_file5.splitlines()
        self.section.append(Setting('check_links', True))
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results, [])

    def test_blockquote_indentation(self):
        content = blockquote_indentation_file.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].message,
                                 'Remove 1 space between blockquote and '
                                 'content')
                self.assertEqual(results[0].severity, RESULT_SEVERITY.NORMAL)

    def test_checkbox_content_indentation(self):
        content = checkbox_content_indentation_file.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].message,
                                 'Checkboxes should be followed by a single '
                                 'character')
                self.assertEqual(results[0].severity, RESULT_SEVERITY.NORMAL)

    def test_codeblock_style_unused_definition(self):
        content = labels_at_eof_unused_definition_file.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].message,
                                 'Move definitions to the end of the file '
                                 '(after the node at line `5`)')
                self.assertEqual(results[0].severity, RESULT_SEVERITY.NORMAL)
                self.assertEqual(results[1].message,
                                 'Found unused definition')
                self.assertEqual(results[1].severity, RESULT_SEVERITY.NORMAL)

    def test_first_heading_level(self):
        content = first_heading_level_file.splitlines()
        self.section.append(Setting('first_heading_level', 2))
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].message,
                                 'First heading level should be `2`')
                self.assertEqual(results[0].severity, RESULT_SEVERITY.NORMAL)

    def test_heading_level_increment(self):
        content = heading_level_increment_file.splitlines()
        self.section.append(Setting('enforce_heading_level_increment', True))
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].message,
                                 'Heading levels should increment by one '
                                 'level at a time')
                self.assertEqual(results[0].severity, RESULT_SEVERITY.NORMAL)

    def test_empty_url(self):
        content = empty_url_file.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].message,
                                 'Don’t use links without URL')
                self.assertEqual(results[0].severity, RESULT_SEVERITY.NORMAL)
                self.assertEqual(results[1].message,
                                 'Don’t use images without URL')
                self.assertEqual(results[1].severity, RESULT_SEVERITY.NORMAL)

    def test_duplicate_headings(self):
        content = duplicate_heading_file.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].message,
                                 'Do not use headings with similar content '
                                 'per section (3:1)')
                self.assertEqual(results[0].severity, RESULT_SEVERITY.NORMAL)

    def test_punctuations_in_heading(self):
        content = punctuation_in_heading_file.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].message,
                                 'Don’t add a trailing `:` to headings')
                self.assertEqual(results[0].severity, RESULT_SEVERITY.NORMAL)
                self.assertEqual(results[1].message,
                                 'Don’t add a trailing `?` to headings')
                self.assertEqual(results[1].severity, RESULT_SEVERITY.NORMAL)
                self.assertEqual(results[2].message,
                                 'Don’t add a trailing `!` to headings')
                self.assertEqual(results[2].severity, RESULT_SEVERITY.NORMAL)

    def test_html_in_markdown(self):
        content = html_file.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].message,
                                 'Do not use HTML in markdown')
                self.assertEqual(results[0].severity, RESULT_SEVERITY.NORMAL)
