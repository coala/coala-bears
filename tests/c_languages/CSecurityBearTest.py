from bears.c_languages.CSecurityBear import CSecurityBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """
void demo() {
}""".splitlines(keepends=True)


bad_file1 = """
void demo(char *a) {
    strcpy(a, '\n');  // CWE 120
}""".splitlines(keepends=True)


bad_file2 = """
char buf[1024];
ssizet_t len;
if ((len = readlink("/modules/pass1", buf, sizeof(buf)-1)) != -1)
    buf[len] = '\0';
""".splitlines(keepends=True)


CSecurityBearTest = verify_local_bear(
    CSecurityBear,
    valid_files=(good_file,),
    invalid_files=(bad_file1, bad_file2))
