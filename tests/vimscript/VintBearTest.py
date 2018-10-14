from bears.vimscript.VintBear import VintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


good_file = """
:let foo = 'bar'
:echo foo
"""


bad_file = """
:let foo = "bar"
:echo foo
"""


VintBearTest = verify_local_bear(VintBear,
                                 valid_files=(good_file,),
                                 invalid_files=(bad_file,))
