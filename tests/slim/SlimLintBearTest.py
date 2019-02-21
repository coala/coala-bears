import os
from queue import Queue

from bears.slim.SlimLintBear import SlimLintBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@generate_skip_decorator(SlimLintBear)
class SlimLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('test section')
        self.uut = SlimLintBear(self.section, Queue())
        test_files = os.path.join(os.path.dirname(__file__), 'test_files')
        self.good_file = os.path.join(test_files, 'good_file.slim')
        self.bad_file = os.path.join(test_files, 'bad_file.slim')
        self.config_file = os.path.join(test_files, 'slim_config.yml')

    def test_run(self):
        self.check_validity(self.uut, [], self.good_file)
        self.check_invalidity(self.uut, [], self.bad_file)

        self.section.append(Setting('slimlint_config', self.config_file))
        self.check_validity(self.uut, [], self.good_file)
        self.check_validity(self.uut, [], self.bad_file)
