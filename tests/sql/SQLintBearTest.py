from bears.sql.SQLintBear import SQLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
SELECT * FROM table_name;
"""

bad_file = """
invalid_SELECT 1;
"""


SQLintBearTest = verify_local_bear(SQLintBear,
                                   valid_files=(good_file,),
                                   invalid_files=(bad_file,))
