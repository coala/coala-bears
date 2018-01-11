import os.path
import unittest
from queue import Queue

from bears.ruby.RubySecurityBear import RubySecurityBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'brakeman_test_files',
                        name)


@generate_skip_decorator(RubySecurityBear)
class RubySecurityBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('brakeman')
        self.queue = Queue()
        self.file_dict = {}
        self.test_files = ['**']
        self.uut = RubySecurityBear(self.file_dict,
                                    self.section,
                                    self.queue)

    def get_results(self, files_to_check):
        files = [get_testfile_path(file) for file in files_to_check]
        for filename in files:
            self.file_dict[filename] = tuple(filename)
        return list(self.uut.run_bear_from_section([], {}))

    def test_warning_with_value_code(self):
        results = self.get_results(self.test_files)
        messages = [result.message for result in results]
        self.assertEqual("'Evaluation' (in 'eval(params)'): "
                         'User input in eval.', messages[1])

    def test_warning_without_value_code(self):
        results = self.get_results(self.test_files)
        messages = [result.message for result in results]
        self.assertEqual("'ValidationRegex': Insufficient validation "
                         "for 'name' using /^[a-zA-Z]+$/. Use "
                         r'\A and \z as anchors', messages[0])
