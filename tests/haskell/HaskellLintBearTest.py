from bears.haskell.HaskellLintBear import HaskellLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
myconcat = (++)
"""

bad_file = """
myconcat a b = ((++) a b)
"""

HaskellLintBearTest = verify_local_bear(HaskellLintBear,
                                        valid_files=(good_file,),
                                        invalid_files=(bad_file,),
                                        tempfile_kwargs={'suffix': '.hs'})
