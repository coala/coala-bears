from queue import Queue
from shutil import which
from unittest.case import skipIf

from bears.python.FutureBear import FutureBear
from coalib.settings.Section import Section
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper


@skipIf(which('futurize') is None, 'futurize is not installed')
class FutureBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('test section')
        self.uut = FutureBear(self.section, Queue())

        self.test_lines = [
            "print 'Hello World!'\n\n",
            "d = {1: 'a', 2: 'b', 3: 'c'}\n\n",
            'for k, v in d.iteritems():\n',
            "    print '{}: {}'.format(k, v)\n"
        ]

    def test_base(self):
        self.check_validity(self.uut,
                            self.test_lines,
                            valid=False)
