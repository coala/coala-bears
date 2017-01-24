from bears.css.StyleLintBear import StyleLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
a {
  color: #fff;
}
"""

bad_file = """
a {
  color: #FFF;
}
"""

StyleLintBearTest = verify_local_bear(StyleLintBear,
                                      valid_files=(good_file,),
                                      invalid_files=(bad_file,))
