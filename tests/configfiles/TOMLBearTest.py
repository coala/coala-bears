from bears.configfiles.TOMLBear import TOMLBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
best-day-ever = 1987-07-05T17:45:00Z
pi = 3.14
negpi = -3.14
"""

bad_file = """
no-leads = 1987-7-05T17:45:00Z
answer = .12345
neganswer = -.12345
"""

TOMLBearTest = verify_local_bear(TOMLBear,
                                 valid_files=(good_file,),
                                 invalid_files=(bad_file,))
