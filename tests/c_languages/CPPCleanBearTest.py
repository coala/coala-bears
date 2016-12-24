from bears.c_languages.CPPCleanBear import CPPCleanBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
int main() {
    return 0;
}
"""


bad_file = """
int global_var = 3;

int main() {
    return 0;
}
"""


CPPCleanBearTest = verify_local_bear(CPPCleanBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,))
