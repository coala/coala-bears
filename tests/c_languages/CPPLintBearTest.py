from bears.c_languages.CPPLintBear import CPPLintBear
from tests.LocalBearTestHelper import LocalBearTestHelper, verify_local_bear
from queue import Queue
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from tests.BearTestHelper import generate_skip_decorator

test_file = """
int main() {
    return 0;
}
"""

CPPLintBearTest = verify_local_bear(CPPLintBear,
                                    valid_files=(),
                                    invalid_files=(test_file,),
                                    tempfile_kwargs={"suffix": ".cpp"})

CPPLintBearIgnoreConfigTest = verify_local_bear(
        CPPLintBear,
        valid_files=(test_file,),
        invalid_files=(),
        settings={'cpplint_ignore': 'legal'},
        tempfile_kwargs={"suffix": ".cpp"})

CPPLintBearLineLengthConfigTest = verify_local_bear(
        CPPLintBear,
        valid_files=(),
        invalid_files=(test_file,),
        settings={'cpplint_ignore': 'legal',
                  'max_line_length': '13'},
        tempfile_kwargs={"suffix": ".cpp"})


@generate_skip_decorator(CPPLintBear)
class CPPLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section("test section")
        # uut = unit under test
        self.uut = CPPLintBear(self.section, Queue())

    def test_config_failure_use_spaces(self):
        self.section["use_spaces"] = "False"
        self.section.append(Setting('use_spaces', "False"))
        with self.assertRaises(AssertionError):
            self.check_validity(self.uut, [], test_file)

    def test_config_success_indent_size(self):
        self.section["indent_size"] = "2"
        self.section.append(Setting('indent_size', "2"))
        self.check_validity(self.uut, [], test_file)

    def test_config_failure_indent_size(self):
        self.section["indent_size"] = "4"
        self.section.append(Setting('indent_size', "4"))
        with self.assertRaises(AssertionError):
            self.check_validity(self.uut, [], test_file)
