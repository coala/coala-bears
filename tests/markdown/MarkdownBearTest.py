import unittest
from queue import Queue

from bears.markdown.MarkdownBear import MarkdownBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import verify_local_bear, execute_bear
from coalib.settings.Section import Section
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

Read more [This does not exist](#world).
"""

test_file5 = """# World

Read more [This exists](#world).
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

MarkdownBearValidateLinksTest = verify_local_bear(
    MarkdownBear,
    valid_files=(test_file5,),
    invalid_files=(test_file4,))


@generate_skip_decorator(MarkdownBear)
class MarkdownBearValidateLinksResultMessageTest(unittest.TestCase):

    def setUp(self):
        self.uut = MarkdownBear(Section('name'), Queue())

    def test_validate_links_message(self):
        content = test_file4.splitlines()
        with prepare_file(content, None) as (file, fname):
            with execute_bear(self.uut, fname, file) as results:
                self.assertEqual(results[0].message,
                                 'Link to unknown heading: `world`')
