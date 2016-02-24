from bears.python.RadonBear import RadonBear
from tests.LocalBearTestHelper import verify_local_bear

test_file1 = """
def simple():
    pass
""".splitlines(keepends=True)


test_file2 = """
class class1():
    pass
""".splitlines(keepends=True)


RadonBearNoReportsTest = verify_local_bear(RadonBear,
                                           valid_files=(test_file1, test_file2),
                                           invalid_files=(),
                                           settings={
                                               "radon_ranks_info": "",
                                               "radon_ranks_normal": "",
                                               "radon_ranks_major": ""})


RadonBearReportsTest = verify_local_bear(RadonBear,
                                         valid_files=(),
                                         invalid_files=(test_file1, test_file2),
                                         settings={
                                             "radon_ranks_info": "",
                                             "radon_ranks_normal": "A",
                                             "radon_ranks_major": ""})
