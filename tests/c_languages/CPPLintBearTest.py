from bears.c_languages.CPPLintBear import CPPLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

test_file = """
int main() {
    return 0;
}
"""

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

CPPLintBearIndentSizeConfigTest = verify_local_bear(
    CPPLintBear,
    valid_files=(),
    invalid_files=(test_file,),
    settings={'cpplint_ignore': 'legal',
              'use_spaces': 'False'},
    tempfile_kwargs={'suffix': '.cpp'})

CPPLintBearUseSpacesConfigTest = verify_local_bear(
    CPPLintBear,
    valid_files=(),
    invalid_files=(test_file),
    settings={'cpplint_ignore': 'legal',
              'indent_size': '4'},
    tempfile_kwargs={'suffix': '.cpp'},)
