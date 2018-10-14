import os
from bears.c_languages.CPPCleanBear import CPPCleanBear
from coalib.testing.LocalBearTestHelper import verify_local_bear
from coala_utils.string_processing import escape

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


test_include_paths_file = """
#include "foo.h"
#include "bar.h"

int main() {
    foo();
    bar();
    return 0;
}
"""


def get_testdirectory_name(test_directory):
    return os.path.join(os.path.dirname(__file__),
                        'test_files',
                        test_directory)


CPPCleanBearTest = verify_local_bear(CPPCleanBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,
                                                    test_include_paths_file,),
                                     tempfile_kwargs={'suffix': '.cpp'})

CPPCleanBearValidIncludeMultiplePathTest = verify_local_bear(
    CPPCleanBear,
    valid_files=(test_include_paths_file,),
    invalid_files=(),
    settings={'include_paths':
              escape(get_testdirectory_name('headers1'), '\\') + ',' +
              escape(get_testdirectory_name('headers2'), '\\')},
    tempfile_kwargs={'suffix': '.cpp'})

CPPCleanBearInvalidIncludeSinglePathTest = verify_local_bear(
    CPPCleanBear,
    valid_files=(),
    invalid_files=(test_include_paths_file,),
    settings={'include_paths':
              escape(get_testdirectory_name('headers1'), '\\')},
    tempfile_kwargs={'suffix': '.cpp'})
