from bears.css.CSSAutoPrefixBear import CSSAutoPrefixBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


good_file = """
.example {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
}
"""

bad_file = """
.example {
    display: flex;
}
"""

CSSAutoPrefixBear = verify_local_bear(CSSAutoPrefixBear,
                                      valid_files=(good_file,),
                                      invalid_files=(bad_file,))
