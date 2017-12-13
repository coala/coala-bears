import os
import unittest
from queue import Queue

from bears.c_languages.CPPCheckBear import CPPCheckBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


def get_absolute_test_path(file):
    return os.path.join(os.path.dirname(__file__),
                        'cppcheck_test_files', file)


@generate_skip_decorator(CPPCheckBear)
class CPPCheckBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('cppcheck')
        self.file_dict = {}
        self.queue = Queue()
        self.test_files = ['good_file.cpp', 'bad_file.cpp', 'warn_file.cpp']

    def get_results(self, files_to_check):
        files = [get_absolute_test_path(file) for file in files_to_check]
        for filename in files:
            with open(filename, 'r', encoding='utf-8') as content:
                self.file_dict[filename] = tuple(content.readlines())
        self.uut = CPPCheckBear(self.file_dict,
                                self.section,
                                self.queue)
        return list(self.uut.run_bear_from_section([], {}))

    def test_results_complete(self):
        self.section.append(Setting('enable', 'unusedFunction'))
        results = self.get_results(self.test_files)
        messages = [result.message for result in results]
        self.assertEqual(len(messages), 2)
        self.assertRegex(messages[0], 'Array .+ out of bounds')
        self.assertRegex(messages[1], "function 'f1' .+ never used")

    def test_no_enable_entered(self):
        results = self.get_results(self.test_files)
        messages = [result.message for result in results]
        self.assertEqual(len(messages), 1)
        self.assertRegex(messages[0], 'Array .+ out of bounds')
        self.assertNotRegex(messages[0], 'function .+ never used')
