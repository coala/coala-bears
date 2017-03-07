import os

from bears.c_languages.AStyleLintBear import AStyleLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

test_file1 = """
int main()
{
    int a = 19;
    return 0;
}\n"""

test_file2 = """
int main() {
    int a = 19;
    return 0;
}\n"""

test_file3 = """
int main() {
\tint a = 12;
\treturn 0;
}\n"""

test_file4 = """
int main()
{
        int a=23;
        return 0;
}\n"""


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__), 'astyle_test_files',  name)


AStyleLintBearTestUseJavaStyle = verify_local_bear(
                     AStyleLintBear,
                     valid_files=(test_file1,),
                     invalid_files=(test_file2,),
                     settings={'astyle_style': 'allman'}
                 )

AStyleLintBearTestUseSpaces = verify_local_bear(
                    AStyleLintBear,
                    valid_files=(test_file1,),
                    invalid_files=(test_file3,),
                    settings={'use_spaces': True}
                )

AStyleLintBearTestUseTabs = verify_local_bear(
                    AStyleLintBear,
                    valid_files=(test_file3,),
                    invalid_files=(test_file2,),
                    settings={'use_spaces': False}
                )

AStyleLintBearTestIndentFourSpaces = verify_local_bear(
                    AStyleLintBear,
                    valid_files=(test_file1,),
                    invalid_files=(test_file4,),
                    settings={'use_spaces': True,
                              'indent_size': 4}
                )

AStyleLintBearTestUseOptionsFile = verify_local_bear(
                    AStyleLintBear,
                    valid_files=(test_file1,),
                    invalid_files=(test_file2,),
                    settings={'astyle_config': get_testfile_path(
                        'astylerc_file')}
                )
