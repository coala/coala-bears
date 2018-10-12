import logging
import os
import unittest
from queue import Queue

from bears.c_languages.CPPCheckBear import CPPCheckBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.bearlib.languages.Language import Language


def get_absolute_test_path(file):
    return os.path.join(os.path.dirname(__file__),
                        'cppcheck_test_files', file)


@generate_skip_decorator(CPPCheckBear)
class CPPCheckBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('cppcheck')
        self.file_dict = {}
        self.queue = Queue()
        self.test_files = ['good_file.cpp', 'bad_file.cpp', 'warn_file.cpp',
                           'language_test.cpp']

    def get_results(self, files_to_check):
        files = [get_absolute_test_path(file) for file in files_to_check]
        for filename in files:
            with open(filename, 'r', encoding='utf-8') as content:
                self.file_dict[filename] = tuple(content.readlines())
        self.uut = CPPCheckBear(self.file_dict,
                                self.section,
                                self.queue)

        result = self.uut.run_bear_from_section([], {})
        if result is not None:
            return list(result)
        return

    def test_results_complete_language_cpp(self):
        self.section.append(Setting('enable', 'unusedFunction'))
        self.section.append(Setting('language', 'c++'))
        self.section.language = Language['c++']
        results = self.get_results(self.test_files)
        self.assertEqual(isinstance(results, list), True)
        messages = [result.message for result in results]
        self.assertEqual(len(messages), 4)
        self.assertRegex(messages[0], 'Array .+ out of bounds')
        self.assertRegex(messages[1], 'When .+ out of bounds')
        self.assertRegex(messages[2], "function 'f1' .+ never used")
        self.assertRegex(messages[3], "function 'foo' .+ never used")

    def test_language_c(self):
        self.section.append(Setting('language', 'c'))
        self.section.language = Language['c']
        results = self.get_results(self.test_files)
        self.assertEqual(isinstance(results, list), True)
        messages = [result.message for result in results]
        self.assertEqual(len(messages), 1)
        self.assertRegex(messages[0], 'Array .+ out of bounds')

    def test_no_enable_no_language_entered(self):
        results = self.get_results(self.test_files)
        self.assertEqual(isinstance(results, list), True)
        messages = [result.message for result in results]
        self.assertEqual(len(messages), 2)
        self.assertRegex(messages[0], 'Array .+ out of bounds')
        self.assertNotRegex(messages[0], 'function .+ never used')
        self.assertRegex(messages[1], 'When .+ out of bounds')

    def test_undefined_language_entered(self):
        self.section.append(Setting('language', 'undefined'))
        with self.assertLogs(logging.getLogger()) as log:
            self.get_results(self.test_files)
            self.assertEqual(
                log.output, ['ERROR:root:Language can be either c or c++'])

    def test_wrong_language_entered(self):
        self.section.append(Setting('language', 'Python'))
        self.section.language = Language['Python']
        with self.assertLogs(logging.getLogger()) as log:
            self.get_results(self.test_files)
            self.assertEqual(
                log.output, ['ERROR:root:Language can be either c or c++'])
