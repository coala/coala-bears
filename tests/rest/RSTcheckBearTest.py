from bears.rest.RSTcheckBear import RSTcheckBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

rst_syntax_good = '====\ntest\n====\n'
rst_syntax_bad = '====\ntest\n===\n'

python_block_good = '====\nTest\n====\n.. code-block:: python\n\n    print()'
python_block_bad = '====\nTest\n====\n.. code-block:: python\n\n    print(\n'

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
