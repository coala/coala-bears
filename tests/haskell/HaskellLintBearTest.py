from bears.haskell.HaskellLintBear import HaskellLintBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """
myconcat = (++)
""".splitlines(keepends=True)

bad_file = """
myconcat a b = ((++) a b)
""".splitlines(keepends=True)

HaskellLintBearTest = verify_local_bear(HaskellLintBear,
                                        valid_files=(good_file,),
                                        invalid_files=(bad_file,),
                                        tempfile_kwargs={"suffix": ".hs"})
