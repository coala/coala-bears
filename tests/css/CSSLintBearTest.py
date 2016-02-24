from bears.css.CSSLintBear import CSSLintBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """
.class {
  font-weight: 400;
  font-size: 5px;
}
""".splitlines(keepends=True)


bad_file = """
.class {
  font-weight: 400
  font-size: 5px;
}
""".splitlines(keepends=True)


CSSLintBearTest = verify_local_bear(CSSLintBear,
                                    valid_files=(good_file,),
                                    invalid_files=(bad_file,))
