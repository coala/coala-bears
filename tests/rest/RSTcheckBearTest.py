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

good_directive1 = '''
===
Foo
===

.. one::
    Foo
'''

good_directive2 = '''
===
Bar
===

.. one::
    Foo

.. two::
    Bar
'''

bad_directive = '''
===
Bar
===

.. three::
    Hello
'''

good_role = '''
Foo
===

:src:`hello_world.py`
:RFC:`793`
'''

bad_role = '''
Bar
===

:bad:`345`
'''

RSTcheckBearIgnoreDirectiveTest = verify_local_bear(
    RSTcheckBear,
    valid_files=(good_directive1, good_directive2,),
    invalid_files=(bad_directive,),
    settings={'directive_ignore': 'one, two'})

RSTcheckBearIgnoreRoleTest = verify_local_bear(
    RSTcheckBear,
    valid_files=(good_role,),
    invalid_files=(good_directive1, good_directive2, bad_role,),
    settings={'role_ignore': 'src, RFC'})
