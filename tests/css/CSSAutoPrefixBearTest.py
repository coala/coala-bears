from bears.css.CSSAutoPrefixBear import CSSAutoPrefixBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
.example {
    display: -webkit-box;
    display: -webkit-flex;
    display: -ms-flexbox;
    display: flex;
}
""".splitlines(keepends=True)

bad_file = """
.example {
    display: flex;
}
""".splitlines(keepends=True)

CSSAutoPrefixBear = verify_local_bear(CSSAutoPrefixBear,
                                      valid_files=(good_file,),
                                      invalid_files=(bad_file,))
