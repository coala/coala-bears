import os
from queue import Queue

from bears.apertium.ApertiumLintBear import ApertiumLintBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@generate_skip_decorator(ApertiumLintBear)
class ApertiumLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('test section')
        self.uut = ApertiumLintBear(self.section, Queue())
        test_files = os.path.join(os.path.dirname(__file__), 'test_files')
        self.good_file = os.path.join(test_files, 'apertium-go-od.en.dix')
        self.bad_file = os.path.join(test_files, 'apertium-ba-ad.en.dix')
        self.config_file = os.path.join(test_files, 'apertium_config.json')

    def test_run(self):
        self.section.append(Setting('apertiumlint_config', ''))
        self.check_validity(self.uut, [], self.good_file)

        self.section.append(Setting('apertiumlint_config', self.config_file))
        self.check_validity(self.uut, [], self.good_file)

        self.section.append(Setting('apertiumlint_config', ''))
        self.check_invalidity(self.uut, [], self.bad_file)

        self.section.append(Setting('apertiumlint_config', self.config_file))
        self.check_invalidity(self.uut, [], self.bad_file)

    def test_paradigm_names(self):
        self.section.append(Setting('paradigm_names', 'False'))
        self.check_validity(self.uut, [], self.bad_file)
