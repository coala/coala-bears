import os
import unittest
from queue import Queue

from bears.python.PyreBear import PyreBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section


@generate_skip_decorator(PyreBear)
class PyreBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('pyre')
        self.queue = Queue()
        test_folder = os.path.join(os.path.dirname(__file__),
                                   'pyre_test_files')
        self.test_good_file = os.path.join(test_folder,
                                           'pyre_test_good/pyre_good.py')
        self.test_bad_file = os.path.join(test_folder,
                                          'pyre_test_bad/pyre_bad.py')

    def get_results(self, file):
        file_dict = {}
        with open(file, 'r', encoding='utf-8') as content:
            file_dict[file] = tuple(content.readlines())
        self.uut = PyreBear(file_dict,
                            self.section,
                            self.queue)
        if self.uut.run_bear_from_section([], {}) is None:
            return []
        return list(self.uut.run_bear_from_section([], {}))

    def test_bad_file_result(self):
        results = self.get_results(self.test_bad_file)
        # Check result message(s)
        messages = [result.message for result in results]
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0], 'Incompatible return type [7]: '
                         'Expected `int` but got `str`.')
        self.assertEqual(messages[1], 'Incompatible return type [7]: '
                         'Expected `str` but got `int`.')
        # Check results lines & columns
        lines = [result.affected_code[0] for result in results]
        # For message #1
        self.assertEqual(lines[0].end.column, 5)
        self.assertEqual(lines[0].start.column, 5)
        self.assertEqual(lines[0].end.line, 2)
        self.assertEqual(lines[0].start.line, 2)
        # For message #2
        self.assertEqual(lines[1].end.column, 5)
        self.assertEqual(lines[1].start.column, 5)
        self.assertEqual(lines[1].end.line, 6)
        self.assertEqual(lines[1].start.line, 6)

    def test_good_file_result(self):
        results = self.get_results(self.test_good_file)
        # Check result message
        self.assertEqual(len(results), 0)
