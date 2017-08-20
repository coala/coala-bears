import re
import unittest

from bears.rest.RSTcheckBear import RSTcheckBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

rst_syntax_good = '====\ntest\n====\n'
rst_syntax_bad = '====\ntest\n===\n'

python_block_good = '====\nTest\n====\n.. code-block:: python\n\n    print()'
python_block_bad = '====\nTest\n====\n.. code-block:: python\n\n    print(\n'


good_file2 = ':doc:`here <../Users/Tutorial>`'
bad_file2 = '==test\n==='


def test_ignore_unknown(errors):
    for error in errors:
        msg = error.full_message
    unittest.assertRegex('[\w|\-]+', re)
    unittest.assertEqual(
        msg,
        'No directive entry for "argparse" in module'
        '"docutils.parsers.rst.languages.en"'
    )


RSTcheckBearTest_ignore_no_code_block = verify_local_bear(
                RSTcheckBear,
                (rst_syntax_good, python_block_good),
                (rst_syntax_bad, python_block_bad),
                )
RSTcheckBearTest_ignore_python_code_block = verify_local_bear(
                RSTcheckBear,
                (rst_syntax_good, python_block_bad, python_block_good),
                (rst_syntax_bad,),
                settings={'code_block_language_ignore': 'python'})
RSTcheckBearTest_ignore_directives = verify_local_bear(
                RSTcheckBear,
                valid_files=(good_file2,),
                invalid_files=(bad_file2,),
                settings={'--ignore-directives': True})
