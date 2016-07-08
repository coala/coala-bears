from queue import Queue
import unittest
import os

from bears.general.AnnotationBear import AnnotationBear
from coala_utils.string_processing.Core import escape
from coalib.results.SourceRange import SourceRange
from coalib.results.AbsolutePosition import AbsolutePosition
from coalib. results.HiddenResult import HiddenResult
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from tests.LocalBearTestHelper import execute_bear


class AnnotationBearTest(unittest.TestCase):

    def setUp(self):
        self.section1 = Section("")
        self.section1.append(Setting('language', 'python3'))
        self.python_uut = AnnotationBear(self.section1, Queue())
        self.section2 = Section("")
        self.section2.append(Setting('language', 'c'))
        self.c_uut = AnnotationBear(self.section2, Queue())

    def test_single_line_string(self):
        text = ["'from start till the end with #comments'\n", ]
        compare = (SourceRange.from_absolute_position(
                                    "F",
                                    AbsolutePosition(text, 0),
                                    AbsolutePosition(text, len(text[0]) - 2)),)
        with execute_bear(self.python_uut, "F", text) as result:
            self.assertEqual(result[0].contents['strings'], compare)
            self.assertEqual(result[0].contents['comments'], ())

        text = ["a'\n", "b'\n"]
        with execute_bear(self.python_uut, "F", text) as result:
            self.assertEqual(result[0].message, "' has no closure")

    def test_multiline_string(self):
        text = ["'''multiline string, #comment within it'''\n"]
        compare = (SourceRange.from_absolute_position(
                        "F",
                        AbsolutePosition(text, 0),
                        AbsolutePosition(text, len(text[0])-2)),)
        with execute_bear(self.python_uut, "F", text) as result:
            self.assertEqual(result[0].contents['strings'], compare)
            self.assertEqual(result[0].contents['comments'], ())

    def test_single_line_comment(self):
        text = ["some #coment with 'string'\n", "and next line"]
        compare = (SourceRange.from_absolute_position(
                                    "F",
                                    AbsolutePosition(text, text[0].find('#')),
                                    AbsolutePosition(text, len(text[0]) - 1)),)
        with execute_bear(self.python_uut, "F", text) as result:
            self.assertEqual(result[0].contents['strings'], ())
            self.assertEqual(result[0].contents['comments'], compare)

    def test_multiline_comment(self):
        text = ["some string /*within \n", "'multiline comment'*/"]
        compare = (SourceRange.from_absolute_position(
                            "F",
                            AbsolutePosition(text, text[0].find('/*')),
                            AbsolutePosition(text, len(''.join(text)) - 1)),)
        with execute_bear(self.c_uut, "F", text) as result:
            self.assertEqual(result[0].contents['strings'], ())
            self.assertEqual(result[0].contents['comments'], compare)

        text = ['/*Multiline which does not end']
        with execute_bear(self.c_uut, "F", text) as result:
            self.assertEqual(result[0].message, '/* has no closure')

    def test_string_with_comments(self):
        text = ["some #comment\n", "with 'string' in  next line"]
        comment_start = text[0].find('#')
        comment_end = len(text[0]) - 1
        string_start = ''.join(text).find("'")
        string_end = ''.join(text).find("'", string_start + 1)
        compare = [(SourceRange.from_absolute_position(
                                "F",
                                AbsolutePosition(text, string_start),
                                AbsolutePosition(text, string_end)),),
                   (SourceRange.from_absolute_position(
                                "F",
                                AbsolutePosition(text, comment_start),
                                AbsolutePosition(text, comment_end)),)]
        with execute_bear(self.python_uut, "F", text) as result:
            self.assertEqual(result[0].contents['strings'], compare[0])
            self.assertEqual(result[0].contents['comments'], compare[1])

    def test_combined_strings(self):
        file_text = ['"some string #with comment"\n',
                     '"""\n',
                     "now a multiline string ''' <- this one not\n",
                     '"""\n',
                     '"""\n'
                     'another comment # rather harmless\n',
                     '"""\n']
        string1_start = 0
        string1_end = len(file_text[0]) - 2
        string1 = SourceRange.from_absolute_position(
                                    "F",
                                    AbsolutePosition(file_text, string1_start),
                                    AbsolutePosition(file_text, string1_end))
        string2_start = string1_end+2
        text = ''.join(file_text)
        string2_end = text.find('"""', string2_start + 1) + 2
        #+2 for length of """
        string2 = SourceRange.from_absolute_position(
                                    "F",
                                    AbsolutePosition(file_text, string2_start),
                                    AbsolutePosition(file_text, string2_end))
        string3_start = text.find('"""', string2_end + 1)
        string3_end = text.find('"""', string3_start + 1) + 2
        #+2 for length of """
        string3 = SourceRange.from_absolute_position(
                                    "F",
                                    AbsolutePosition(file_text, string3_start),
                                    AbsolutePosition(file_text, string3_end))
        with execute_bear(self.python_uut, "F", file_text) as results:
            self.assertIn(string1, results[0].contents['strings'])
            self.assertIn(string2, results[0].contents['strings'])
            self.assertIn(string3, results[0].contents['strings'])
            self.assertEqual(results[0].contents['comments'], ())

    def test_external_coalang(self):
        self.section1.append(Setting('coalang_dir', escape(os.path.join(
                            os.path.dirname(__file__), 'test_files'), '\\')))
        self.section1.append(Setting('language', 'test'))
        uut = AnnotationBear(self.section1, Queue())
        text = ['//comment line 1\n', '"""string line 2"""']
        with execute_bear(uut, "F", text) as result:
            self.assertNotEqual(result[0].contents['strings'], ())
            self.assertNotEqual(result[0].contents['comments'], ())
