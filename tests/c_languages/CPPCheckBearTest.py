from bears.c_languages.CPPCheckBear import CPPCheckBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """
using namespace std;
int main() {
    cout << "Hello, world!" << endl;
    return 0;
}""".splitlines(keepends=True)

warn_file = """
void f1(struct fred_t *p)
{
    int x;
    if (p)
        do_something(x);
}""".splitlines(keepends=True)

bad_file = """
#define f(c) { \
    char *p = new char[10];  \
    p[c] = 42; \
}
int main() {
    f(100);
    return 0;
}""".splitlines(keepends=True)


CPPCheckBearTest1 = verify_local_bear(CPPCheckBear,
                                      valid_files=(good_file, warn_file),
                                      invalid_files=(bad_file,))

CPPCheckBearTest2 = verify_local_bear(CPPCheckBear,
                                      valid_files=(good_file,),
                                      invalid_files=(warn_file, bad_file),
                                      settings={'enable': 'unusedFunction'})
