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
