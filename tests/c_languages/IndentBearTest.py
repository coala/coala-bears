from bears.c_languages.IndentBear import IndentBear
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


IndentBearTest = verify_local_bear(IndentBear,
                                   valid_files=(test_file1,),
                                   invalid_files=(test_file2,
                                                  test_file3,
                                                  test_file4),
                                   settings={"use_spaces": "true",
                                             "max_line_length": "80"})


IndentBearWithTabTest = verify_local_bear(IndentBear,
                                          valid_files=(test_file3,),
                                          invalid_files=(test_file1,
                                                         test_file2,
                                                         test_file4),
                                          settings={"use_spaces": "nope",
                                                    "max_line_length": "80"})


IndentBearIndentWidthTest = verify_local_bear(IndentBear,
                                              valid_files=(test_file2,),
                                              invalid_files=(test_file1,
                                                             test_file3,
                                                             test_file4),
                                              settings={"use_spaces": "true",
                                                        "max_line_length": "80",
                                                        "tab_width": "2"})
