import os
from bears.c_languages.CPPCheckBear import CPPCheckBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """
using namespace std;
int main() {
    cout << "Hello, world!" << endl;
    return 0;
}"""

warn_file = """
void f1(struct fred_t *p)
{
    int x;
    if (p)
        do_something(x);
}"""

bad_file = """
#define f(c) { \
    char s[10]; \
    s[c] = 42; \
}
int main() {
    f(100);
    return 0;
}"""

test_dir = os.path.join(os.path.dirname(__file__), 'test_files')

CPPCheckBearTest1 = verify_local_bear(CPPCheckBear,
                                      valid_files=(good_file, warn_file),
                                      invalid_files=(bad_file,),
                                      settings={'include_paths': test_dir})

CPPCheckBearTest2 = verify_local_bear(CPPCheckBear,
                                      valid_files=(good_file,),
                                      invalid_files=(warn_file, bad_file),
                                      settings={'enable': 'unusedFunction'})
