from bears.r.FormatRBear import FormatRBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file_1 = """1 + 1
if (TRUE) {
    x = 1  # inline comments
} else {
    x = 2
    print("Oh no... ask the right bracket to go away!")
}"""


good_file_2 = """1 + 1
if (TRUE) {
    x <- 1  # inline comments
} else {
    x <- 2
    print("Oh no... ask the right bracket to go away!")
}"""


good_file_3 = """1 + 1
if (TRUE) {
    x = 1
} else {
    x = 2
    print("Oh no... ask the right bracket to go away!")
}"""


good_file_4 = """1 + 1
if (TRUE)
{
    x = 1  # inline comments
} else
{
    x = 2
    print("Oh no... ask the right bracket to go away!")
}"""


good_file_5 = """1 + 1
if (TRUE) {
        x = 1  # inline comments
} else {
        x = 2
        print("Oh no... ask the right bracket to go away!")
}"""


good_file_6 = """x = (1 + 1 + 1 + 1 + 1 + 1 +\x20
    1 + 1 + 1)
if (TRUE) {
    x = 1  # inline comments
} else {
    x = 2
    print("Oh no... ask the right bracket to go away!")
}
"""

good_file_7 = """1 + 1
if (TRUE) {
    x = 1  # inline comments
} else {
    x <- 2
    print("Oh no... ask the right bracket to go away!")
}
"""

bad_file_1 = """1+1
if(TRUE){
x=1  # inline comments
}else{x=2;print("Oh no... ask the right bracket to go away!")}
"""


bad_file_2 = """1+1


if(TRUE){
x=1  # inline comments
}else{
x=2;print("Oh no... ask the right bracket to go away!")}
"""


bad_file_3 = """x=(1+1+1+1+1+1+1+1+1)
if(TRUE){
x=1  # inline comments
}else{x=2;print("Oh no... ask the right bracket to go away!")}
"""


FormatRBearTest = verify_local_bear(
    FormatRBear,
    valid_files=(good_file_1,),
    invalid_files=(bad_file_1,))


FormatRBearRArrowToEqualTest = verify_local_bear(
    FormatRBear,
    valid_files=(good_file_2,),
    invalid_files=(bad_file_1,),
    settings={'r_use_arrows': 'true'})


FormatRBearRKeepCommentsTest = verify_local_bear(
    FormatRBear,
    valid_files=(good_file_3,),
    invalid_files=(good_file_1,),
    settings={'r_keep_comments': 'false'})


FormatRBearRBraceToNewlineTest = verify_local_bear(
    FormatRBear,
    valid_files=(good_file_4,),
    invalid_files=(bad_file_1,),
    settings={'r_braces_on_next_line': 'true'})


FormatRBearRKeepBlanklinesTest = verify_local_bear(
    FormatRBear,
    valid_files=(good_file_1,),
    invalid_files=(bad_file_2,),
    settings={'r_keep_blank_lines': 'false'})


FormatRBearRTabwidthTest = verify_local_bear(
    FormatRBear,
    valid_files=(good_file_5,),
    invalid_files=(bad_file_1,),
    settings={'indent_size': '8'})


FormatRBearRWidthcutoffTest = verify_local_bear(
    FormatRBear,
    valid_files=(good_file_6,),
    invalid_files=(bad_file_3,),
    settings={'r_max_expression_length': '25'})

FormatRBearDefaultSettingsTest = verify_local_bear(
    FormatRBear,
    valid_files=(good_file_7,),
    invalid_files=(bad_file_3,),
    settings={})
