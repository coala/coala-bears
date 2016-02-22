from bears.sql.SQLintBear import SQLintBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """
SELECT * FROM table_name;
""".splitlines(True)

bad_file = """
invalid_SELECT 1;
""".splitlines(True)


SQLintBearTest = verify_local_bear(SQLintBear,
                                   valid_files=(good_file,),
                                   invalid_files=(bad_file,))
