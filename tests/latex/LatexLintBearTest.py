from bears.latex.LatexLintBear import LatexLintBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
{.}
{ sometext }\\
""".splitlines(keepends=True)


bad_file = """
{ .}
{ Sometext \\
""".splitlines(keepends=True)


LatexLintBearTest = verify_local_bear(LatexLintBear,
                                      valid_files=(good_file,),
                                      invalid_files=(bad_file,))
