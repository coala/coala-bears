import os
import re
from queue import Queue
from shutil import which
from unittest.case import skipIf

from bears.css.StyleLintBear import StyleLintBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@skipIf(which('stylelint') is None, 'Stylelint is not installed')
class StyleLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('test section')
        self.uut = StyleLintBear(self.section, Queue())
        test_files = os.path.join(os.path.dirname(__file__), 'test_files')
        self.good_file = os.path.join(test_files, 'stylelint_good.css')
        self.bad_file = os.path.join(test_files, 'stylelint_bad.css')

    def test_run(self):
        self.check_validity(self.uut, [], self.good_file)
        self.check_validity(self.uut, [], self.bad_file, valid=False)
