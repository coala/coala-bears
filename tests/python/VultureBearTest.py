from bears.python.VultureBear import VultureBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
x = 2
print(x)
"""

bad_file = """
b = 10
a = 12
print(a)
"""

VultureBear = verify_local_bear(VultureBear,
                                valid_files=(good_file,),
                                invalid_files=(bad_file,))
