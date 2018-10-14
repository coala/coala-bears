from bears.latex.LatexLintBear import LatexLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


good_file = """
{.}
{ sometext }\\
"""


bad_file = """
{ .}
{ Sometext \\
"""


LatexLintBearTest = verify_local_bear(LatexLintBear,
                                      valid_files=(good_file,),
                                      invalid_files=(bad_file,))
