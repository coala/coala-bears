import os
from queue import Queue
from shutil import which
from unittest.case import skipIf

from bears.go.GoVetBear import GoVetBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.settings.Section import Section


@skipIf(which('go') is None, 'go is not installed')
class GoVetBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('test section')
        self.uut = GoVetBear(self.section, Queue())

    def test_syntax_error(self):
        good_file = os.path.join(os.path.dirname(__file__),
                                 'test_files',
                                 'vet_good.go')
        bad_file = os.path.join(os.path.dirname(__file__),
                                'test_files',
                                'vet_bad_semantics.go')
        self.check_validity(self.uut, [], good_file)
        self.check_invalidity(self.uut, [], bad_file)

    def test_semantic_error(self):
        bad_file = os.path.join(os.path.dirname(__file__),
                                'test_files',
                                'vet_bad_syntax.go')
        self.check_invalidity(self.uut, [], bad_file)
