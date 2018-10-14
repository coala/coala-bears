from bears.hypertext.HTMLLintBear import HTMLLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

test_file = """
<html>
  <body>
    <h1>Hello, world!</h1>
  </body>
</html>
"""

test_ignore_tabs = """
<html>
    <body>
        <h1>Hello, world!</h1>
    </body>
</html>
"""

HTMLLintBearTest = verify_local_bear(HTMLLintBear,
                                     valid_files=(),
                                     invalid_files=(test_file,),
                                     settings={'use_spaces': 'False'},
                                     tempfile_kwargs={'suffix': '.html'})

HTMLLintBearIgnoreTest = verify_local_bear(
    HTMLLintBear,
    valid_files=(test_file,),
    invalid_files=(),
    settings={'use_spaces': 'False', 'htmllint_ignore': 'optional_tag'},
    tempfile_kwargs={'suffix': '.html'})

HTMLLintBearIgnoreQuotationTest = verify_local_bear(
    HTMLLintBear,
    valid_files=(),
    invalid_files=(test_file,),
    settings={'use_spaces': 'False', 'htmllint_ignore': 'quotation'},
    tempfile_kwargs={'suffix': '.html'})

HTMLLintBearIgnoreTabs = verify_local_bear(
    HTMLLintBear,
    valid_files=(test_file,),
    invalid_files=(test_ignore_tabs,),
    settings={'use_spaces': 'True', 'htmllint_ignore': 'optional_tag'},
    tempfile_kwargs={'suffix': '.html'})
