from bears.c_languages.CPPCleanBear import CPPCleanBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """
int main() {
    return 0;
}
""".splitlines(keepends=True)


bad_file = """
int global_var = 3;

int main() {
    return 0;
}
""".splitlines(keepends=True)


CPPCleanBearTest = verify_local_bear(CPPCleanBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,))
