from bears.c_languages.CPPCleanBear import CPPCleanBear
from coalib.testing.LocalBearTestHelper import verify_local_bear
import os

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

test_file = """
include "CPPCleanBearHeaderTest.h"

int main() {
	cppcleanbearfunction();
    return 0;
}
"""


CPPCleanBearTest = verify_local_bear(CPPCleanBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,),
                                     tempfile_kwargs={'suffix': '.cpp'})

CPPLintBearIncludePathTest2 = verify_local_bear(
    CPPCleanBear,
    valid_files=(),
    invalid_files=(test_file,),
    tempfile_kwargs={'suffix': '.cpp'}
    )

CPPLintBearIncludePathTest = verify_local_bear(
    CPPCleanBear,
    valid_files=(test_file,),
    invalid_files=(),
    settings={'include_path': os.path.join(os.path.dirname(__file__),
                                           'test_files',
                                           'CPPCleanBearHeaderTest.h')},
    tempfile_kwargs={'suffix': '.cpp'}
    )
