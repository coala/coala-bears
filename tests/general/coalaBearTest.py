from bears.general.coalaBear import coalaBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
coala"""

bad_file_1 = """
Coala"""

bad_file_2 = """
COALA"""

bad_file_3 = """
CoAla"""

coalaBearTest = verify_local_bear(
    coalaBear,
    valid_files=(good_file,),
    invalid_files=(bad_file_1, bad_file_2, bad_file_3))
