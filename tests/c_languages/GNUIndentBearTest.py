from bears.c_languages.GNUIndentBear import GNUIndentBear
from tests.LocalBearTestHelper import verify_local_bear

test_file1 = """
int
main ()
{
    return 0;
}""".splitlines(keepends=True)


test_file2 = """
int
main ()
{
  return 0;
}""".splitlines(keepends=True)


test_file3 = """
int
main ()
{
\treturn 0;
}""".splitlines(keepends=True)


test_file4 = """
int main() {
  return 0;
}""".splitlines(keepends=True)


test_file5 = """
int
main ()
{
  int a;
  return 0;
}""".splitlines(keepends=True)


test_file6 = """
int
main ()
{
    int a;

    return 0;
}""".splitlines(keepends=True)


GNUIndentBearTest = verify_local_bear(
    GNUIndentBear,
    valid_files=(test_file1,),
    invalid_files=(test_file2, test_file3, test_file4),
    settings={"use_spaces": "true", "max_line_length": "80"})


GNUIndentBearWithTabTest = verify_local_bear(
    GNUIndentBear,
    valid_files=(test_file3,),
    invalid_files=(test_file1, test_file2, test_file4),
    settings={"use_spaces": "nope", "max_line_length": "80"})


GNUIndentBearWidthTest = verify_local_bear(
    GNUIndentBear,
    valid_files=(test_file2,),
    invalid_files=(test_file1, test_file3, test_file4),
    settings={"use_spaces": "true", "max_line_length": "80", "tab_width": "2"})


GNUIndentBearBlankLineAfterDeclarationsTest = verify_local_bear(
    GNUIndentBear,
    valid_files=(test_file6,),
    invalid_files=(test_file5,),
    settings={"blank_lines_after_declarations": "true"})
