import os
from queue import Queue

from bears.c_languages.CPPCheckBear import CPPCheckBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


def get_absolute_test_path(file):
    return os.path.join(os.path.dirname(__file__),
                        'cppcheck_test_files', file)


@generate_skip_decorator(CPPCheckBear)
class CPPCheckBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('cppcheck')
        self.uut = CPPCheckBear(self.section, Queue())
        self.good_file = get_absolute_test_path('good_file.cpp')
        self.bad_file = get_absolute_test_path('bad_file.cpp')
        self.warn_file = get_absolute_test_path('warn_file.cpp')

    def test_default(self):
        self.check_validity(self.uut, [], self.good_file)
        self.check_invalidity(self.uut, [], self.bad_file)
        self.check_validity(self.uut, [], self.warn_file)

    def test_enable(self):
        self.section.append(Setting('enable', 'unusedFunction'))
        self.check_validity(self.uut, [], self.good_file)
        self.check_invalidity(self.uut, [], self.bad_file)
        self.check_invalidity(self.uut, [], self.warn_file)
