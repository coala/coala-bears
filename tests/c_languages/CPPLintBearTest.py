from bears.c_languages.CPPLintBear import CPPLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear,\
    LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
import queue

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

    def setUp(self):
        self.section = Section('name')
        self.uut = CPPLintBear(self.section,
                               queue.Queue())

    def test_use_spaces_config(self):
        settings = {'cpplint_ignore': 'legal',
                    'use_spaces': 'False'}
        for name, value in settings.items():
            self.section.append(Setting(name, value))
        with self.assertRaisesRegex(AssertionError, 'Bear returned None'
                                                    ' on execution\n'):
            self.check_validity(self.uut,
                                test_file.splitlines(keepends=True),
                                valid=False)

    def test_indent_size_config(self):
        settings = {'cpplint_ignore': 'legal',
                    'indent_size': '4'}
        for name, value in settings.items():
            self.section.append(Setting(name, value))
        with self.assertRaisesRegex(AssertionError, 'Bear returned None'
                                                    ' on execution\n'):
            self.check_validity(self.uut,
                                test_file.splitlines(keepends=True),
                                valid=False)
