from bears.c_languages.GNUIndentBear import GNUIndentBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

test_file1 = """
int
main ()
{
    return 0;
}"""


test_file2 = """
int
main ()
{
  return 0;
}"""


test_file3 = """
int
main ()
{
\treturn 0;
}"""


test_file4 = """
int main() {
  return 0;
}"""


test_file5 = """
int
main ()
{

  int a;
  return 0;
}"""


test_file6 = """
int
main ()
{

    int a;

    return 0;
}"""


test_file7 = """
int
main ()
{
    int a;

    return 0;
}"""


test_file8 = """
if (bool)
{
    return a;
}
else
{
}"""


test_file9 = """
if (bool) {
    return a;
} else {
}"""


test_file10 = """
int main()
{
    return 0;
}"""


GNUIndentBearTest = verify_local_bear(
    GNUIndentBear,
    valid_files=(test_file1,),
    invalid_files=(test_file2, test_file3, test_file4),
    settings={'use_spaces': 'true', 'max_line_length': '79'})


GNUIndentBearWithTabTest = verify_local_bear(
    GNUIndentBear,
    valid_files=(test_file3,),
    invalid_files=(test_file1, test_file2, test_file4),
    settings={'use_spaces': 'nope', 'max_line_length': '79'})


GNUIndentBearWidthTest = verify_local_bear(
    GNUIndentBear,
    valid_files=(test_file2,),
    invalid_files=(test_file1, test_file3, test_file4),
    settings={'use_spaces': 'true', 'max_line_length': '79',
              'indent_size': '2'})


GNUIndentBearBlankLineAfterDeclarationsTest = verify_local_bear(
    GNUIndentBear,
    valid_files=(test_file6,),
    invalid_files=(test_file5,),
    settings={'blank_lines_after_declarations': 'true'})


GNUIndentBearBraceOnIfLineAndCuddlElseTest = verify_local_bear(
    GNUIndentBear,
    valid_files=(test_file9,),
    invalid_files=(test_file8,),
    settings={'braces_on_if_line': 'true', 'cuddle_else': 'true'})


GNUIndentBearDeleteOptionalBlankLinesTest = verify_local_bear(
    GNUIndentBear,
    valid_files=(test_file7,),
    invalid_files=(test_file5,),
    settings={'delete_optional_blank_lines': 'false'})


GNUIndentBearGNUStyleTest = verify_local_bear(
    GNUIndentBear,
    valid_files=(test_file2,),
    invalid_files=(test_file4,),
    settings={'gnu_style': 'true'})


GNUIndentBearKandRStyleTest = verify_local_bear(
    GNUIndentBear,
    valid_files=(test_file10,),
    invalid_files=(test_file1,),
    settings={'k_and_r_style': 'true'})
