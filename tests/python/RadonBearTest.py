from queue import Queue

from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section
from bears.python.RadonBear import RadonBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.LocalBearTestHelper import verify_local_bear

test_file1 = """
def simple():
    pass
"""


test_file2 = """
class class1():
    pass
"""

test_file3 = 'def f():\n' + ('    assert True\n' * 50)


# Tests for deprecated settings
RadonBearRanksDefaultsTest = verify_local_bear(
    RadonBear,
    valid_files=(test_file1, test_file2),
    invalid_files=(test_file3,))


RadonBearRanksNoReportsTest = verify_local_bear(
    RadonBear,
    valid_files=(test_file1, test_file2, test_file3),
    invalid_files=(),
    settings={'radon_ranks_info': '',
              'radon_ranks_normal': '',
              'radon_ranks_major': ''})


RadonBearRanksReportsTest = verify_local_bear(
    RadonBear,
    valid_files=(),
    invalid_files=(test_file1, test_file2),
    settings={'radon_ranks_info': '',
              'radon_ranks_normal': 'A',
              'radon_ranks_major': ''})


# Tests for new settings
class RadonBearTest(LocalBearTestHelper):
    def setUp(self):
        self.section = Section('test')
        self.uut = RadonBear(self.section, Queue())

    def test_cyclomatic_complexity(self):
        # Test for info results
        self.check_results(
            self.uut,
            test_file3.splitlines(True),
            [Result.from_values('RadonBear',
                                'f has a cyclomatic complexity of 51',
                                severity=RESULT_SEVERITY.INFO,
                                file='test_file3',
                                line=1,
                                end_line=1)],
            filename='test_file3',
            settings={'cyclomatic_complexity': 52})

        # Test for major results
        self.check_results(
            self.uut,
            test_file3.splitlines(True),
            [Result.from_values('RadonBear',
                                'f has a cyclomatic complexity of 51',
                                severity=RESULT_SEVERITY.MAJOR,
                                file='test_file3',
                                line=1,
                                end_line=1)],
            filename='test_file3',
            settings={'cyclomatic_complexity': 10})
