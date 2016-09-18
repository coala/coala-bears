from bears.css.CSSCombBear import CSSCombBear
from tests.LocalBearTestHelper import verify_local_bear
import os

test_simple = """
example {
    color: red;
}
"""
test_file_space_before_colon = """
example {
    color: red;
}
"""
test_file_multiple = """
example {
    content: "secure"
    background-color: lightblue
}
"""
test_file_multiple_semicolon = """
example {
    content: 'secure';
    background-color: lightblue;
}
"""
test_file_space_before_colon2 = """
example {
    color : red;
}
"""
test_file2 = """
example {color: red}
"""

test_file3 = """
example {
color: red;
background-color: lightblue}
"""

test_file4 = """
example {
color: red;
margin-bottom: 100px;
margin-right: 150px;
margin-left: 80px}
"""

test_file5 = """
example{
    color: red;
    margin-bottom: 100px;
    margin-right: 150px;
}
"""
test_file6 = """
example{color :red;
}
"""
test_file_space_after_colon = """
a {
    color: red;
}
"""
test_file_force_semicolon = """
example{
    color:red
}
"""

test_file_space_after = """
example {
    margin-bottom: 100px;
}
"""

test_file_space_after_close_brace = """
example {
    margin-bottom: 100px;
}
"""

test_file_remove_empty_rulesets = """
example {
    margin-bottom: 100px;
}
example2 {}
"""

test_file_add_semicolon = """
example {
    margin-bottom: 200px
}
"""

test_file_color_case = """
example {
    color: #fff;
}
"""

test_file_color_upper = """
example {
    color: #FFF;
}
"""

test_file_block_indent = """
example {
color: tomato;
}
"""

test_file_block_indent_tab = """
example {
    color:tomato;
}
"""

csscombconfig = os.path.join(os.path.dirname(__file__),
                             "test_files",
                             "csscomb.json")

settings = {
    "force_semicolon": True,
    "color_case": "upper",
    "eof_newline": True,
    "leading_zero": False,
    "sort_order_fallback": True,
    "space_before_colon": True,
    "space_after_colon": True,
    "strip_spaces": True,
    "sort_order_fallback": True,
    "space_before_o_brace": True,
    "space_after_o_brace": True,
    "space_before_colon": True,
    "space_after_colon": True}

CSSCombBearTest = verify_local_bear(CSSCombBear,
                                    valid_files=(test_simple,),
                                    invalid_files=(test_file2,
                                                   test_file3, test_file4))


CSSCombBearConfigFileTest = verify_local_bear(
    CSSCombBear,
    valid_files=(test_file5,),
    invalid_files=(test_file2, test_file3),
    settings={"csscomb_json": csscombconfig})


CSSCombBearSemicolonTest = verify_local_bear(
    CSSCombBear,
    invalid_files=(test_file_force_semicolon,),
    valid_files=(test_simple,),
    settings={"force_semicolon": True})


CSSCombBearSpaceBefore = verify_local_bear(
    CSSCombBear,
    invalid_files=(test_file_space_before_colon,),
    valid_files=(test_file_space_before_colon2,),
    settings={"space_before_colon": True})


CSSCombBearSpaceAfter = verify_local_bear(
    CSSCombBear,
    invalid_files=(test_file2, test_file4),
    valid_files=(test_file_space_after_colon,),
    settings={"space_after_colon": True})


CSSCombBearSpaceAfter2 = verify_local_bear(
    CSSCombBear,
    invalid_files=(test_file3, test_file4),
    valid_files=(test_simple,),
    settings={"space_after_colon": True,
              "space_before_c_brace": True})


CSSCombBearSpaceAfter3 = verify_local_bear(
    CSSCombBear,
    invalid_files=(test_file3, test_file4, test_file2),
    valid_files=(test_file6),
    settings={"space_after_colon": False,
              "space_before_c_brace": True,
              "strip_spaces": True})


CSSCombBearSpaceAfter4 = verify_local_bear(
    CSSCombBear,
    invalid_files=(test_file_multiple,),
    valid_files=(test_file_space_after_close_brace, test_simple),
    settings={"space_after_colon": True,
              "space_before_c_brace": True,
              "strip_spaces": True,
              "vendor_prefix_align": True,
              "quotes": "single",
              "leading_zero": False})


CSSCombBearSpaceAfter5 = verify_local_bear(
    CSSCombBear,
    invalid_files=(test_file3, test_file4, test_file2),
    valid_files=(test_file_multiple_semicolon,),
    settings={"space_after_colon": True,
              "space_before_c_brace": True,
              "strip_spaces": True,
              "vendor_prefix_align": True,
              "quotes": "single",
              "leading_zero": False})


CSSCombBearSpaceAfterMultiple = verify_local_bear(
    CSSCombBear,
    invalid_files=(test_file_multiple,),
    valid_files=(test_file_space_after_close_brace, test_simple),
    settings={"space_after_colon": True,
              "space_before_c_brace": True,
              "strip_spaces": True,
              "vendor_prefix_align": True,
              "quotes": "single",
              "leading_zero": False,
              "eof_newline": True,
              "block_indent": "\t"})


CSSCombBearRulesetsTest = verify_local_bear(
    CSSCombBear,
    invalid_files=(test_file_remove_empty_rulesets,),
    valid_files=(test_simple,),
    settings={"remove_empty_rulesets": True})


CSSCombBearSemicolonTestTrue = verify_local_bear(
    CSSCombBear,
    invalid_files=(test_file_add_semicolon,),
    valid_files=(test_simple,),
    settings={"force_semicolon": True})


CSSCombBearColorCaseTest = verify_local_bear(
    CSSCombBear,
    invalid_files=(test_file_color_case,),
    valid_files=(test_file_color_upper,),
    settings={"color_case": "upper"})

CSSCombBearBlockIndent = verify_local_bear(
    CSSCombBear,
    invalid_files=(test_file_block_indent),
    valid_files=(test_file_block_indent_tab,),
    settings={"block_indent": "\t"}
)
