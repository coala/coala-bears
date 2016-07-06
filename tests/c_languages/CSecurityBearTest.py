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


good_file1 = """
void demo(char *a) {
    strcpy(a, 'c');  // Flawfinder: ignore
}""".splitlines(keepends=True)


CSecurityBearTest = verify_local_bear(
    CSecurityBear,
    valid_files=(good_file,),
    invalid_files=(bad_file1, bad_file2, good_file1),
    settings={"neverignore": "true"})


CSecurityBearIgnoreTest = verify_local_bear(
    CSecurityBear,
    valid_files=(good_file1, good_file),
    invalid_files=(bad_file2,),
    settings={"neverignore": "false"})
