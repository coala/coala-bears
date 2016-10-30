from bears.csv.CSVLintBear import CSVLintBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """id,first_name,last_name,email,gender,ip_address
1,Cynthia,Rogers,crogers0@nasa.gov,Female,158.131.39.207
2,Lisa,Carroll,lcarroll1@elegantthemes.com,Female,157.69.195.53
3,Kevin,Baker,kbaker2@imageshack.us,Male,113.189.69.4
"""


bad_file = """id,first_name,last_name,email,gender,ip_address
1,Cynthia,Rogers,crogers0@nasa.gov,Female,158.131.39.207
2,Lisa,Carroll,lcarroll1@elegantthemes.com,157.69.195.53
3,Kevin,Baker,kbaker2@imageshack.us,Male,113.189.69.4
"""


CSVLintBearTest = verify_local_bear(CSVLintBear,
                                    valid_files=(good_file,),
                                    invalid_files=(bad_file,))
