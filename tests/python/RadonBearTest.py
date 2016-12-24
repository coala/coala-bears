from bears.python.RadonBear import RadonBear
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


RadonBearDefaultsTest = verify_local_bear(
    RadonBear,
    valid_files=(test_file1, test_file2),
    invalid_files=(test_file3,))


RadonBearNoReportsTest = verify_local_bear(
    RadonBear,
    valid_files=(test_file1, test_file2, test_file3),
    invalid_files=(),
    settings={'radon_ranks_info': '',
              'radon_ranks_normal': '',
              'radon_ranks_major': ''})


RadonBearReportsTest = verify_local_bear(
    RadonBear,
    valid_files=(),
    invalid_files=(test_file1, test_file2),
    settings={'radon_ranks_info': '',
              'radon_ranks_normal': 'A',
              'radon_ranks_major': ''})
