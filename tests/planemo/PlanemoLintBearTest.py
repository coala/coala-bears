import os
from queue import Queue
from shutil import which
from unittest.case import skipIf

from bears.planemo.PlanemoLintBear import PlanemoLintBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section


@skipIf(which('planemo') is None, 'Planemo is not installed')
class PlanemoLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('test section')
        self.uut = PlanemoLintBear(self.section, Queue())
        self.test_file = os.path.join(os.path.dirname(__file__),
                                      'test_files',
                                      'planemolint_test.xml')

    def test_run(self):
        self.check_validity(
            self.uut,
            [],  # Doesn't matter, planemo lint will parse the file
            self.test_file,
            valid=False)
        self.test_file = os.path.join(os.path.dirname(__file__),
                                      'test_files',
                                      'valid_planemo_test.xml')
        self.check_validity(
            self.uut,
            [],  # Doesn't matter, planemo lint will parse the file
            self.test_file,
            valid=True)
