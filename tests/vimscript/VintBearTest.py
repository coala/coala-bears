from bears.vimscript.VintBear import VintBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
:let foo = 'bar'
:echo foo
""".splitlines(keepends=True)


bad_file = """
:let foo = "bar"
:echo foo
""".splitlines(keepends=True)


VintBearTest = verify_local_bear(VintBear,
                                 valid_files=(good_file,),
                                 invalid_files=(bad_file,))
