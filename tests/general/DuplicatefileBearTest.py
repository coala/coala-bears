import unittest
import os

from coalib.settings.Section import Section
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from bears.general.DuplicateFileBear import DuplicateFileBear
from queue import Queue


def get_absolute_test_path(file):
    return os.path.join(os.path.dirname(__file__),
                        'duplicate_test_files', file)


class DuplicateFileBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('name')
        self.queue = Queue()
        self.file_dict = {}
        self.test_files = ['complexFirst.txt', 'complexSecond.txt',
                           'noMatch.txt', 'smallFirst.txt',
                           'smallSecond.txt']

    def get_results(self, files_to_check):
        self.files = [get_absolute_test_path(file) for file in files_to_check]
        for filename in self.files:
            with open(filename, 'r', encoding='utf-8') as _file:
                self.file_dict[filename] = tuple(_file.readlines())
        self.maxDiff = None
        self.uut = DuplicateFileBear(self.file_dict, self.section,
                                     self.queue)
        return list(self.uut.run())

    def test_results_complete(self):
        results = self.get_results(self.test_files)
        messages = [result.message for result in results]
        combined = '\t'.join(messages)
        self.assertIn(get_absolute_test_path(
            'complexSecond.txt'), combined.split())
        self.assertIn(get_absolute_test_path(
            'complexFirst.txt'), combined.split())
        self.assertIn(get_absolute_test_path(
            'smallFirst.txt'), combined.split())
        self.assertIn(get_absolute_test_path(
            'smallSecond.txt'), combined.split())
        self.assertEquals(results[0].severity, RESULT_SEVERITY.INFO)

    def test_results_no_duplicates(self):
        results = self.get_results([self.test_files[2],
                                    self.test_files[3]])
        messages = [result.message for result in results]
        self.assertEquals(messages, [])

    def test_results_empty(self):
        results = self.get_results([])
        messages = [result.message for result in results]
        self.assertEquals(messages, ['You did not add any file to compare'])
        self.assertEquals(results[0].severity, RESULT_SEVERITY.MAJOR)

    def test_result_single(self):
        results = self.get_results([self.test_files[0]])
        messages = [result.message for result in results]
        self.assertEquals(messages, ['You included only one file'])
        self.assertEquals(results[0].severity, RESULT_SEVERITY.MAJOR)
