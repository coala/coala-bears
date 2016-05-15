from bears.c_languages.CSecurityBear import CSecurityBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
void demo() {
}""".splitlines(keepends=True)

bad_file = """
void demo(char *a) {
    strcpy(a, '\n');  // CWE 120
}""".splitlines(keepends=True)


CSecurityBearTest = verify_local_bear(CSecurityBear,
                                      valid_files=(good_file,),
                                      invalid_files=(bad_file,))
