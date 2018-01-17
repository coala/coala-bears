import unittest
import os
from queue import Queue

from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from bears.gherkin.GherkinLintBear import GherkinLintBear
from coalib.testing.BearTestHelper import generate_skip_decorator


@generate_skip_decorator(GherkinLintBear)
class GherkinLintBearTest(unittest.TestCase):

    def setUp(self):
        self.section = Section('Gherkin')
        self.queue = Queue()
        self.file_dict = {}
        self.uut = GherkinLintBear(self.file_dict, self.section, self.queue)

    def set_config_dir(self, directory):
        test_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), directory))
        self.uut.get_config_dir = lambda *args, **kwargs: test_path

    def test_dup_feature_names(self):
        self.set_config_dir('test_files')
        self.section.append(Setting('allow_dupe_feature_names', False))
        results = list(self.uut.run_bear_from_section([], {}))
        self.assertTrue(len(results) == 1)
        self.assertEqual(results[0].message,
                         'Feature name is already used in: ' +
                         'DuplicateFeatureName-Pt1.feature')

    def test_no_settings(self):
        self.set_config_dir('test_files1')
        results = list(self.uut.run_bear_from_section([], {}))
        self.assertTrue(len(results) == 0)

    def test_default_settings(self):
        self.set_config_dir('test_files2')
        results = list(self.uut.run_bear_from_section([], {}))
        self.assertTrue(len(results) == 3)

    def test_config_file(self):
        config_file = os.path.join(os.path.dirname(__file__),
                                   'config_files',
                                   '.gherkin-lintrc')
        self.section.append(Setting('gherkin_config', config_file))
        self.set_config_dir('test_files1')
        results = list(self.uut.run_bear_from_section([], {}))
        self.assertTrue(len(results) > 10)
