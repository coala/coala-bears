from bears.css.CSSLintBear import CSSLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
.class {
  font-size: 5px;
  font-weight: 400;
}
"""


bad_file = """
.class {
  font-size: 5px
  font-weight: 400;
}
"""


CSSLintBearTest = verify_local_bear(CSSLintBear,
                                    valid_files=(good_file,),
                                    invalid_files=(bad_file,))
