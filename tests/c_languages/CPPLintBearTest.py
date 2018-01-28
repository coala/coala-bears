from bears.c_languages.CPPLintBear import CPPLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

test_file = """
int main() {
    return 0;
}
"""

test_file2 = ('int main() {\n' +
              '    int x;\n' +
              '    x = 3;' * 100 + '\n'
              '    return 0;\n' +
              '}\n')

CPPLintBearTest = verify_local_bear(CPPLintBear,
                                    valid_files=(),
                                    invalid_files=(test_file,),
                                    tempfile_kwargs={'suffix': '.cpp'})

CPPLintBearIgnoreConfigTest = verify_local_bear(
    CPPLintBear,
    valid_files=(test_file,),
    invalid_files=(),
    settings={'cpplint_ignore': 'legal'},
    tempfile_kwargs={'suffix': '.cpp'})

CPPLintBearLineLengthConfigTest = verify_local_bear(
    CPPLintBear,
    valid_files=(),
    invalid_files=(test_file,),
    settings={'cpplint_ignore': 'legal',
              'max_line_length': '13'},
    tempfile_kwargs={'suffix': '.cpp'})

CPPLintBearInfiniteLineLengthTest = verify_local_bear(
    CPPLintBear,
    valid_files=(test_file2,),
    invalid_files=(),
    settings={'max_line_length': '0',
              'cpplint_ignore': 'legal/copyright'},
    tempfile_kwargs={'suffix': '.cpp'})
