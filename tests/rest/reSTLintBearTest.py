from bears.rest.reSTLintBear import reSTLintBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = ["test\n====\n"]
bad_file = ["test\n==\n"]


reSTLintBearTest = verify_local_bear(reSTLintBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,))
