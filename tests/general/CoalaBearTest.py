from bears.general.CoalaBear import CoalaBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """
Coala
COALA
CoAla"""

bad_file_1 = """
coala"""

bad_file_2 = """
cOALA"""

bad_file_3 = """
coAla"""

coalaBearTest = verify_local_bear(
    CoalaBear,
    valid_files=(good_file,),
    invalid_files=(bad_file_1, bad_file_2, bad_file_3))
