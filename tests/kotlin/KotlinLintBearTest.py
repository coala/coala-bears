import os
import unittest
from queue import Queue

from coalib.settings.Section import Section
from bears.kotlin.KotlinLintBear import KotlinLintBear
from coalib.testing.BearTestHelper import generate_skip_decorator


@generate_skip_decorator(KotlinLintBear)
class KotlinLintBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('Kotlin')
        self.queue = Queue()
        self.file_dict = {}
        self.uut = KotlinLintBear(self.file_dict, self.section, self.queue)

    def set_config_dir(self, directory):
        test_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), directory))
        self.uut.get_config_dir = lambda *args, **kwargs: test_path

    def test_bad_files(self):
        self.set_config_dir('bad_files')
        results = list(self.uut.run_bear_from_section([], {}))
        self.assertTrue(len(results) > 10)

    def test_good_files(self):
        self.set_config_dir('good_files')
        results = list(self.uut.run_bear_from_section([], {}))
        self.assertTrue(len(results) == 0)

    def test_config_files(self):
        self.set_config_dir('test_files')
        results = list(self.uut.run_bear_from_section([], {}))
        self.assertTrue(len(results) == 0)
