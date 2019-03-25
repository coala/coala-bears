from queue import Queue

from bears.general.Dos2UnixBear import Dos2UnixBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.results.Result import Result
from coalib.settings.Section import Section

file = r'The 50\'s were swell. \r\n'.splitlines()


class Dos2UnixBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = Dos2UnixBear(Section('name'), Queue())

    def test_run(self):
        self.check_results(
            self.uut,
            file,
            [Result.from_values('Dos2UnixBear',
                                'done',
                                'filename')])
