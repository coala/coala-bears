from bears.scss.SCSSLintBear import SCSSLintBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
.btn-primary {
  &:hover {
    background-color: darken($btn-primary-bg, 3%);
  }
}
""".splitlines(keepends=True)

bad_file = """
.btn-primary {
  &:hover {
    background-color: darken($btn-primary-bg, 3%)
}
""".splitlines(keepends=True)


SCSSLintBearTest = verify_local_bear(SCSSLintBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,))
