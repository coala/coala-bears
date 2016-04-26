from bears.hypertext.HTMLLintBear import HTMLLintBear
from tests.LocalBearTestHelper import verify_local_bear

test_file = """
<html>
  <body>
    <h1>Hello, world!</h1>
  </body>
</html>
""".splitlines(keepends=True)

HTMLLintBearTest = verify_local_bear(HTMLLintBear,
                                     valid_files=(),
                                     invalid_files=(test_file,),
                                     tempfile_kwargs={"suffix": ".html"})

HTMLLintBearIgnoreTest = verify_local_bear(
    HTMLLintBear,
    valid_files=(test_file,),
    invalid_files=(),
    settings={'htmllint_ignore': 'optional_tag'},
    tempfile_kwargs={"suffix": ".html"})

HTMLLintBearIgnoreQuotationTest = verify_local_bear(
    HTMLLintBear,
    valid_files=(),
    invalid_files=(test_file,),
    settings={'htmllint_ignore': 'quotation'},
    tempfile_kwargs={"suffix": ".html"})
