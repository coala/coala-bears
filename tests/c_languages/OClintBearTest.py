from bears.c_languages.OClintBear import OClintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

bad_file = """
int main() {
    int i = 0;
    return 0;
}
"""

good_file = """
using namespace std;
int main() {
    cout << "Hello, world!" << endl;
    return 0;
}
"""


OClintBearTest = verify_local_bear(OClintBear,
                                   valid_files=(good_file,),
                                   invalid_files=(bad_file,))

OClintBearWithSettingsTest = verify_local_bear(
    OClintBear,
    valid_files=(good_file, bad_file),
    invalid_files=(),
    settings={'oclint_cli_options': '-max-priority-3=4'})
