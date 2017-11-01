from queue import Queue

from bears.c_languages.CPPLintBear import CPPLintBear
from coalib.testing.LocalBearTestHelper import (verify_local_bear,
                                                LocalBearTestHelper)
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


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


@generate_skip_decorator(CPPLintBear)
class CPPLintBearTest(LocalBearTestHelper):

    CPP_VALUE_ERROR_RE = 'Bear returned None on execution'

    def setUp(self):
        self.section = Section('test section')
        self.uut = CPPLintBear(self.section, Queue())

    def test_config_failure_indent_size(self):
        self.section.append(Setting('indent_size', 3))
        with self.assertRaisesRegex(AssertionError, self.CPP_VALUE_ERROR_RE):
            self.check_validity(self.uut, [], test_file)

    def test_config_failure_use_spaces(self):
        self.section.append(Setting('use_spaces', False))
        with self.assertRaisesRegex(AssertionError, self.CPP_VALUE_ERROR_RE):
            self.check_validity(self.uut, [], test_file)
