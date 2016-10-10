import unittest
from collections import namedtuple
from queue import Queue

from bears.general.KeywordBear import KeywordBear
from coalib.results.Diff import Diff
from coalib.results.HiddenResult import HiddenResult
from coalib.results.SourceRange import SourceRange
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from tests.LocalBearTestHelper import verify_local_bear, execute_bear

test_file = """
test line fix me
to do
error fixme
"""


KeywordBearTest = verify_local_bear(
    KeywordBear,
    valid_files=(test_file,),
    invalid_files=("test line todo",
                   "test line warNING"),
    settings={"keywords": "todo, warning"})


class KeywordBearTodoTest(unittest.TestCase):

    def setUp(self):
        self.section = Section("")
        self.section.append(Setting('language', 'python3'))
        self.section.append(Setting('keywords', '\# TODO, \#todo'))
        self.python_uut = KeywordBear(self.section, Queue())

        self.annotation_bear_result_type = namedtuple('result', ['contents'])
        self.text = ['# todo 123']
        self.dep_results = {
            'AnnotationBear': [
                self.annotation_bear_result_type({'comments': ()})
            ]
        }
        self.dep_results = {'AnnotationBear': HiddenResult(
            'AnnotationBear', {'comments': ()})}

    def test_todo(self):
        text = ['a == b']

        with execute_bear(self.python_uut, "F", text,
                          dependency_results=self.dep_results) as result:
            self.assertEqual(result, [])

        dep_results = {
            'AnnotationBear': {}
        }
        with execute_bear(self.python_uut, "F", self.text,
                          dependency_results=dep_results) as result:
            self.assertEqual(result[0].diffs, None)
            self.assertEqual(result[0].affected_code[0].start.line, 1)
            self.assertEqual(result[0].affected_code[0].start.column, 1)

        dep_results = {'AnnotationBear': HiddenResult(
            'AnnotationBear', {'comments': 123})}
        with execute_bear(self.python_uut, "F", self.text,
                          dependency_results=dep_results) as result:
            self.assertEqual(result[0].diffs, None)
            self.assertEqual(result[0].affected_code[0].start.line, 1)
            self.assertEqual(result[0].affected_code[0].start.column, 1)

        text = ['# todo 123\n']
        comments = (SourceRange.from_values("F", 1, 1),
                    SourceRange.from_values("F", 1, 40))
        dep_results = {
            'AnnotationBear': [
                self.annotation_bear_result_type({'comments': comments})
            ]
        }

        with execute_bear(self.python_uut, "F", text,
                          dependency_results=dep_results) as result:
            self.assertEqual(result[0].diffs['F'].unified_diff,
                             '--- \n'
                             '+++ \n'
                             '@@ -1 +0,0 @@\n'
                             '-# todo 123\n')

        text = ['test = 55 # todo 123\n']
        comments = (SourceRange.from_values("F", 1, 11),
                    SourceRange.from_values("F", 1, 23))
        dep_results = {
            'AnnotationBear': [
                self.annotation_bear_result_type({'comments': comments})
            ]
        }
        with execute_bear(self.python_uut, "F", text,
                          dependency_results=dep_results) as result:
            self.assertEqual(result[0].diffs['F'].unified_diff,
                             '--- \n'
                             '+++ \n'
                             '@@ -1 +1 @@\n'
                             '-test = 55 # todo 123\n'
                             '+test = 55\n')

    def test_todo_outside_of_comment(self):
        section = Section("")
        section.append(Setting('language', 'python3'))
        section.append(Setting('keywords', 'todo'))
        python_uut = KeywordBear(section, Queue())

        text = ['todo = 123\n']
        with execute_bear(python_uut, "F", text,
                          dependency_results=self.dep_results) as result:
            self.assertIsNone(result[0].diffs)
