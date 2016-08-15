import os

from bears.documentation.DocCapitalizeBear import DocCapitalizeBear
from tests.LocalBearTestHelper import verify_local_bear

with open(os.path.join(os.path.dirname(__file__),
                       "test_files",
                       "DocCapitalizeBear",
                       "bad_file.py")) as bad_f:
    bad_file = bad_f.read()


good_file = """
Hello
"""

DocCapitalizeBear = verify_local_bear(DocCapitalizeBear,
                                      valid_files=(good_file,),
                                      invalid_files=(bad_file,),
                                      settings={'language': 'python',
                                                'docstyle': 'doxygen'})
