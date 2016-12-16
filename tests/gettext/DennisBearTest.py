import os
from queue import Queue


from bears.gettext.DennisBear import DennisBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class DennisBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('test section')
        self.uut = DennisBear(self.section, Queue())
        self.valid_test_file = os.path.join(os.path.dirname(__file__),
                                            'test_files',
                                            'dennis_valid_test.po')
        self.invalid_test_file = os.path.join(os.path.dirname(__file__),
                                              'test_files',
                                              'dennis_invalid_test.po')

    def test_valid(self):
        self.check_validity(self.uut, [], self.valid_test_file)

    def test_invalid(self):
        self.check_validity(self.uut, [], self.invalid_test_file, valid=False)
        # Test without ignoring W302
        self.section.append(Setting('allow_untranslated', 'False'))
        self.check_validity(self.uut, [], self.valid_test_file, valid=False)
