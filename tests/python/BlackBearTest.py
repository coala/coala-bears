from queue import Queue

from bears.python.BlackBear import BlackBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


@generate_skip_decorator(BlackBear)
class BlackBearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section('name')
        self.section.append(Setting('max_line_length', '79'))
        self.uut = BlackBear(self.section, Queue())

    def test_valid(self):
        self.check_validity(self.uut, ['import sys'])
        self.check_validity(self.uut, ['a = [1, 1]'])

    def test_line_length(self):
        self.check_validity(self.uut, ['a = [1, 1]'])
        self.section.append(Setting('max_line_length', '5'))
        self.check_invalidity(self.uut, ['a = [1, 1]'])

    def test_invalid(self):
        self.check_invalidity(self.uut, [''])
        self.check_invalidity(self.uut, ['a=1+1'])
