from queue import Queue

from bears.general.GixyBear import GixyBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.results.Result import Result
from coalib.settings.Section import Section

file = '1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n'


class TooManyLinesBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = GixyBear(Section('name'), Queue())

    def test_run(self):
        self.check_results(
            self.uut,
            file,
            [Result.from_values('GixyBear',
                                'done',
                                file)])
