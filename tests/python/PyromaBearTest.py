import unittest
import os.path
from queue import Queue

from coalib.settings.Section import Section
from bears.python.PyromaBear import PyromaBear


def get_testdir_path(name):
    return os.path.join(os.path.dirname(__file__), 'pyroma_test_files', name)


def get_message_list(results):
    return [result.message for result in results]


class PyromaBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('name')
        self.queue = Queue()
        self.file_dict = {}

    def get_results(self, name):
        setup_file = os.path.join(get_testdir_path(name), 'setup.py')
        if os.path.isfile(setup_file):
            self.file_dict[setup_file] = ''
        self.uut = PyromaBear(self.file_dict, self.section, self.queue)
        return list(self.uut.run())

    def test_complete(self):
        results = self.get_results('complete')
        self.assertEqual(results, [])

    def test_no_setup(self):
        results = self.get_results('no_setup')
        message_list = get_message_list(results)
        self.assertEqual(message_list,
                         ['Your package does not contain a setup file.'])

    def test_minimal(self):
        results = self.get_results('minimal')
        message_list = get_message_list(results)
        self.assertEqual(message_list, [
            "The package's version number does not comply "
            'with PEP-386 or PEP-440.',
            "The package's description should be longer than 10 characters.",
            "The package's long_description is quite short.",
            'Your package does not have classifiers data.',
            'You should specify what Python versions you support.',
            'Your package does not have keywords data.',
            'Your package does not have author data.',
            'Your package does not have author_email data.',
            'Your package does not have url data.',
            'Your package does not have license data.',
            'You are using Setuptools or Distribute but do not specify if '
            'this package is zip_safe or not. You should specify it, as it '
            'defaults to True, which you probably do not want.',
        ])
