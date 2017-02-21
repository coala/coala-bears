import os
import unittest

from queue import Queue

from bears.elixir.CredoBear import CredoBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@generate_skip_decorator(CredoBear)
class CredoBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('name')
        self.queue = Queue()
        self.uut = CredoBear(self.section, self.queue)
        self.start_dir = os.getcwd()
        self.bad_code_test_path = os.path.abspath(os.path.join(
                                                  os.path.dirname(__file__),
                                                  'bad_code')
                                                  )

    def test_readability(self):
        os.chdir(self.bad_code_test_path)
        readability = os.path.abspath(os.path.join(
                                      self.bad_code_test_path,
                                      'lib/readability.ex')
                                      )
        with open(readability) as f:
            content = f.readlines()

        suggestion = self.uut.run(readability, content)
        suggestion = next(suggestion)
        self.assertEqual(suggestion.severity, RESULT_SEVERITY.NORMAL)
        self.assertEqual(suggestion.message, 'Found readability issue.')

    def test_consistency(self):
        os.chdir(self.bad_code_test_path)
        consistency = os.path.abspath(os.path.join(
                                      self.bad_code_test_path,
                                      'lib/consistency.ex')
                                      )
        with open(consistency) as f:
            content = f.readlines()

        suggestion = self.uut.run(consistency, content)
        suggestion = next(suggestion)
        self.assertEqual(suggestion.severity, RESULT_SEVERITY.MAJOR)
        self.assertEqual(suggestion.message, 'Found consistency issue.')

    def test_refactoring(self):
        os.chdir(self.bad_code_test_path)
        refactoring = os.path.abspath(os.path.join(
                                      self.bad_code_test_path,
                                      'lib/refactoring.ex')
                                      )
        with open(refactoring) as f:
            content = f.readlines()

        suggestion = self.uut.run(refactoring, content)
        suggestion = next(suggestion)
        self.assertEqual(suggestion.severity, RESULT_SEVERITY.INFO)
        self.assertEqual(suggestion.message, 'Found refactoring opportunity.')

    def test_warning(self):
        os.chdir(self.bad_code_test_path)
        warning = os.path.abspath(os.path.join(
                                    self.bad_code_test_path,
                                    'lib/warning.ex')
                                  )
        with open(warning) as f:
            content = f.readlines()

        suggestion = self.uut.run(warning, content)
        suggestion = next(suggestion)
        self.assertEqual(suggestion.severity, RESULT_SEVERITY.MAJOR)
        self.assertEqual(suggestion.message,
                         'Found a warning please take a closer look.')

    def test_design(self):
        os.chdir(self.bad_code_test_path)
        design = os.path.abspath(os.path.join(
                                  self.bad_code_test_path,
                                  'lib/design.ex')
                                 )
        with open(design) as f:
            content = f.readlines()

        suggestion = self.uut.run(design, content)
        suggestion = next(suggestion)
        self.assertEqual(suggestion.severity, RESULT_SEVERITY.INFO)
        self.assertEqual(suggestion.message,
                         'Found software design issue.')

    def tearDown(self):
        os.chdir(self.start_dir)
