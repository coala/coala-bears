from queue import Queue
import unittest

from bears.general.AnnotationBear import AnnotationBear
from coalib.results.SourceRange import SourceRange
from coalib.results.AbsolutePosition import AbsolutePosition
from coalib.results.HiddenResult import HiddenResult
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.testing.LocalBearTestHelper import execute_bear


class AnnotationBearTest(unittest.TestCase):

    def setUp(self):
        self.section1 = Section('')
        self.section1.append(Setting('language', 'python 3'))
        self.python_uut = AnnotationBear(self.section1, Queue())
        self.section2 = Section('')
        self.section2.append(Setting('language', 'c'))
        self.c_uut = AnnotationBear(self.section2, Queue())

    def test_single_line_string(self):
        text = ["'from start till the end with #comments'\n", ]
        compare_full = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, 0),
            AbsolutePosition(text, len(text[0]) - 2))

        compare_content = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, 1),
            AbsolutePosition(text, len(text[0]) - 3))

        compare_start = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, 0),
            AbsolutePosition(text, 0))

        compare_end = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, len(text[0]) - 2),
            AbsolutePosition(text, len(text[0]) - 2))

        with execute_bear(self.python_uut, 'F', text) as result:
            for _result in result[0].contents.singleline_strings:
                self.assertEqual(_result.full_range, compare_full)
                self.assertEqual(_result.content_range, compare_content)
                self.assertEqual(
                    _result.start_delimiter_range, compare_start)
                self.assertEqual(_result.end_delimiter_range, compare_end)
            self.assertEqual(result[0].contents.singleline_comments, [])

        text = ["a'\n", "b'\n"]
        with execute_bear(self.python_uut, 'F', text) as result:
            self.assertEqual(result[0].message, "' has no closure")

    def test_empty_string(self):
        text = ["''\n", ]
        compare_full = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, 0),
            AbsolutePosition(text, len(text[0]) - 2))

        compare_start = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, 0),
            AbsolutePosition(text, 0))

        compare_end = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, len(text[0]) - 2),
            AbsolutePosition(text, len(text[0]) - 2))

        with execute_bear(self.python_uut, 'F', text) as result:
            for _result in result[0].contents.singleline_strings:
                self.assertEqual(_result.full_range, compare_full)
                self.assertEqual(_result.content_range, [])
                self.assertEqual(
                    _result.start_delimiter_range, compare_start)
                self.assertEqual(_result.end_delimiter_range, compare_end)
            self.assertEqual(result[0].contents.singleline_comments, [])

    def test_multiline_string(self):
        text = ["'''multiline string, #comment within it'''\n"]
        compare_full = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, 0),
            AbsolutePosition(text, len(text[0]) - 2))

        compare_content = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, 3),
            AbsolutePosition(text, len(text[0]) - 5))

        compare_start = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, 0),
            AbsolutePosition(text, 2))

        compare_end = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, len(text[0]) - 4),
            AbsolutePosition(text, len(text[0]) - 2))

        with execute_bear(self.python_uut, 'F', text) as result:
            for _result in result[0].contents.multiline_strings:
                self.assertEqual(_result.full_range, compare_full)
                self.assertEqual(_result.content_range, compare_content)
                self.assertEqual(
                    _result.start_delimiter_range, compare_start)
                self.assertEqual(_result.end_delimiter_range, compare_end)
            self.assertEqual(result[0].contents.singleline_comments, [])

    def test_single_line_comment(self):
        text = ["some #coment with 'string'\n", 'and next line']
        compare_full = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, text[0].find('#')),
            AbsolutePosition(text, len(text[0]) - 1))

        compare_content = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, text[0].find('#')+1),
            AbsolutePosition(text, len(text[0]) - 2))

        compare_start = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, text[0].find('#')),
            AbsolutePosition(text, text[0].find('#')))

        compare_end = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, len(text[0]) - 1),
            AbsolutePosition(text, len(text[0]) - 1))

        with execute_bear(self.python_uut, 'F', text) as result:
            self.assertEqual(result[0].contents.singleline_strings, [])
            for _result in result[0].contents.singleline_comments:
                self.assertEqual(_result.full_range, compare_full)
                self.assertEqual(_result.content_range, compare_content)
                self.assertEqual(
                    _result.start_delimiter_range, compare_start)
                self.assertEqual(_result.end_delimiter_range, compare_end)

    def test_multiline_comment(self):
        text = ['some string /*within \n', "'multiline comment'*/"]
        compare_full = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, text[0].find('/*')),
            AbsolutePosition(text, len(''.join(text)) - 1))

        compare_content = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, text[0].find('/*')+2),
            AbsolutePosition(text, len(''.join(text)) - 3))

        compare_start = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, text[0].find('/*')),
            AbsolutePosition(text, text[0].find('/*')+1))

        compare_end = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, len(''.join(text)) - 2),
            AbsolutePosition(text, len(''.join(text)) - 1))

        with execute_bear(self.c_uut, 'F', text) as result:
            self.assertEqual(result[0].contents.singleline_strings, [])
            for _result in result[0].contents.multiline_comments:
                self.assertEqual(_result.full_range, compare_full)
                self.assertEqual(_result.content_range, compare_content)
                self.assertEqual(
                    _result.start_delimiter_range, compare_start)
                self.assertEqual(_result.end_delimiter_range, compare_end)

        text = ['/*Multiline which does not end']
        with execute_bear(self.c_uut, 'F', text) as result:
            self.assertEqual(result[0].message, '/* has no closure')

    def test_string_with_comments(self):
        text = ['some #comment\n', "with 'string' in  next line"]
        comment_start = text[0].find('#')
        comment_end = len(text[0]) - 1
        string_start = ''.join(text).find("'")
        string_end = ''.join(text).find("'", string_start + 1)
        compare_full = [SourceRange.from_absolute_position(
                       'F',
                       AbsolutePosition(text, string_start),
                       AbsolutePosition(text, string_end)),
                   SourceRange.from_absolute_position(
                       'F',
                       AbsolutePosition(text, comment_start),
                       AbsolutePosition(text, comment_end))]

        compare_content = [SourceRange.from_absolute_position(
                       'F',
                       AbsolutePosition(text, string_start+1),
                       AbsolutePosition(text, string_end-1)),
                   SourceRange.from_absolute_position(
                       'F',
                       AbsolutePosition(text, comment_start+1),
                       AbsolutePosition(text, comment_end-1))]

        compare_start = [SourceRange.from_absolute_position(
                       'F',
                       AbsolutePosition(text, string_start),
                       AbsolutePosition(text, string_start)),
                   SourceRange.from_absolute_position(
                       'F',
                       AbsolutePosition(text, comment_start),
                       AbsolutePosition(text, comment_start))]

        compare_end = [SourceRange.from_absolute_position(
                       'F',
                       AbsolutePosition(text, string_end),
                       AbsolutePosition(text, string_end)),
                       SourceRange.from_absolute_position(
                       'F',
                       AbsolutePosition(text, comment_end),
                       AbsolutePosition(text, comment_end))]

        with execute_bear(self.python_uut, 'F', text) as result:
            for _result in result[0].contents.singleline_strings:
                self.assertEqual(_result.full_range, compare_full[0])
                self.assertEqual(_result.content_range, compare_content[0])
                self.assertEqual(
                    _result.start_delimiter_range, compare_start[0])
                self.assertEqual(
                    _result.end_delimiter_range, compare_end[0])

            for _result in result[0].contents.singleline_comments:
                self.assertEqual(_result.full_range, compare_full[1])
                self.assertEqual(_result.content_range, compare_content[1])
                self.assertEqual(
                    _result.start_delimiter_range, compare_start[1])
                self.assertEqual(
                    _result.end_delimiter_range, compare_end[1])

    def test_combined_strings(self):
        file_text = ['"some string #with comment"\n',
                     '"""\n',
                     "now a multiline string ''' <- this one not\n",
                     '"""\n',
                     '"""\n'
                     'another comment # rather harmless\n',
                     '"""\n']
        string1_start = 0
        string1_end = len(file_text[0]) - 2  # 2
        string1 = SourceRange.from_absolute_position(
                                    'F',
                                    AbsolutePosition(file_text, string1_start),
                                    AbsolutePosition(file_text, string1_end))

        string_c1 = SourceRange.from_absolute_position(
                                    'F',
                                    AbsolutePosition(
                                        file_text, string1_start+1),
                                    AbsolutePosition(file_text, string1_end-1))

        string_s1 = SourceRange.from_absolute_position(
                                    'F',
                                    AbsolutePosition(file_text, string1_start),
                                    AbsolutePosition(file_text, string1_start))

        string_e1 = SourceRange.from_absolute_position(
                                    'F',
                                    AbsolutePosition(file_text, string1_end),
                                    AbsolutePosition(file_text, string1_end))

        string2_start = string1_end+2
        text = ''.join(file_text)
        string2_end = text.find('"""', string2_start + 1) + 2
        # +2 for length of """
        string2 = SourceRange.from_absolute_position(
                                    'F',
                                    AbsolutePosition(file_text, string2_start),
                                    AbsolutePosition(file_text, string2_end))

        string_c2 = SourceRange.from_absolute_position(
                                    'F',
                                    AbsolutePosition(
                                        file_text, string2_start+3),
                                    AbsolutePosition(file_text, string2_end-3))

        string_s2 = SourceRange.from_absolute_position(
                                    'F',
                                    AbsolutePosition(file_text, string2_start),
                                    AbsolutePosition(file_text,
                                                     string2_start+2))

        string_e2 = SourceRange.from_absolute_position(
                                    'F',
                                    AbsolutePosition(file_text, string2_end-2),
                                    AbsolutePosition(file_text, string2_end))

        string3_start = text.find('"""', string2_end + 1)
        string3_end = text.find('"""', string3_start + 1) + 2
        # +2 for length of """
        string3 = SourceRange.from_absolute_position(
                                    'F',
                                    AbsolutePosition(file_text, string3_start),
                                    AbsolutePosition(file_text, string3_end))

        string_c3 = SourceRange.from_absolute_position(
                                    'F',
                                    AbsolutePosition(
                                        file_text, string3_start+3),
                                    AbsolutePosition(file_text, string3_end-3))

        string_s3 = SourceRange.from_absolute_position(
                                    'F',
                                    AbsolutePosition(file_text, string3_start),
                                    AbsolutePosition(file_text,
                                                     string3_start+2))

        string_e3 = SourceRange.from_absolute_position(
                                    'F',
                                    AbsolutePosition(file_text, string3_end-2),
                                    AbsolutePosition(file_text, string3_end))

        with execute_bear(self.python_uut, 'F', file_text) as results:
            full_ranges = []
            content_ranges = []
            start_delimiter_ranges = []
            end_delimiter_ranges = []
            for _result in (results[0].contents.singleline_strings +
                            results[0].contents.multiline_strings):
                full_ranges.append(_result.full_range)
                content_ranges.append(_result.content_range)
                start_delimiter_ranges.append(_result.start_delimiter_range)
                end_delimiter_ranges.append(_result.end_delimiter_range)

            self.assertIn(string1, full_ranges)
            self.assertIn(string2, full_ranges)
            self.assertIn(string3, full_ranges)

            self.assertIn(string_c1, content_ranges)
            self.assertIn(string_c2, content_ranges)
            self.assertIn(string_c3, content_ranges)

            self.assertIn(string_s1, start_delimiter_ranges)
            self.assertIn(string_s2, start_delimiter_ranges)
            self.assertIn(string_s3, start_delimiter_ranges)

            self.assertIn(string_e1, end_delimiter_ranges)
            self.assertIn(string_e2, end_delimiter_ranges)
            self.assertIn(string_e3, end_delimiter_ranges)

            self.assertEqual(results[0].contents.multiline_comments, [])
            self.assertEqual(results[0].contents.singleline_comments, [])

    def test_no_coalang(self):
        self.section1.append(Setting('language', 'Valyrian'))
        text = ['Valar Morghulis']
        uut = AnnotationBear(self.section1, Queue())
        with execute_bear(uut, 'F', text) as result:
            self.assertEqual(result[0].contents,
                             'coalang specification for Valyrian not found.')

    def test_escape_strings(self):
        text = [r"'I\'ll be back' -T1000"]
        uut = AnnotationBear(self.section1, Queue())
        test_full_range = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, 0),
            AbsolutePosition(text, text[0].find("'", 4)))

        test_content_range = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, 1),
            AbsolutePosition(text, text[0].find("'", 4)-1))

        test_start_range = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, 0),
            AbsolutePosition(text, 0))

        test_end_range = SourceRange.from_absolute_position(
            'F',
            AbsolutePosition(text, text[0].find("'", 4)),
            AbsolutePosition(text, text[0].find("'", 4)))

        with execute_bear(uut, 'F', text) as result:
            self.assertEqual(
                result[0].contents.singleline_strings[0].full_range,
                test_full_range)

            self.assertEqual(
                result[0].contents.singleline_strings[0].content_range,
                test_content_range)

            self.assertEqual(
                result[0].contents.singleline_strings[
                    0].start_delimiter_range,
                test_start_range)

            self.assertEqual(
                result[0].contents.singleline_strings[
                    0].end_delimiter_range,
                test_end_range)

        text = ['''
            """"quoting inside quoting"
            """
            ''']
        uut = AnnotationBear(self.section1, Queue())
        with execute_bear(uut, 'F', text) as results:
            for result in results:
                # The """" was recognized as a string start and end before.
                # That lead to a Result being yielded because of unclosed
                # quotes, this asserts that no such thing happened.
                self.assertEqual(type(result), HiddenResult)
