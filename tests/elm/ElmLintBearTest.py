from queue import Queue

from bears.elm.ElmLintBear import ElmLintBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section
from coalib.testing.LocalBearTestHelper import verify_local_bear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator
from coala_utils.ContextManagers import prepare_file

good_file_no_unexpected_comma = """
ab =
  "Hello World!"
"""

bad_file_unexpected_comma = """
a, b =
  "Hello World!"
"""

good_file_no_unexpected_end_of_input = """
foo =
  100
"""

bad_file_unexpected_end_of_input = """
foo =
"""

good_file_not_empty = """
add x y = x + y
"""

bad_file_empty = """
"""

good_file_comment = """
foo =
  5 * 3 - 8 / 1
-- A single line comment
"""

bad_file_comment = """
-- A single line comment
"""

good_file_list = """
l =
  ["one", "two", "three"]
"""

bad_file_list = """
l =
  ["one", "two", "three"
"""

good_file_function = """
import Html exposing (text)
four =
  sqrt 16
main =
  text (toString [four])
"""

bad_file_function = """
import Html exposing (text)
four =
  sqr 16
main =
  text (toString [four)
"""

result_message_bad_function = """\
text (toString [four)\x1b[31m
                         ^\x1b[0m
I am looking for one of the following things:

    ","
    "]"
    a field access like .name
    an expression
    an infix operator like +
    an infix operator like `andThen`
    more letters in this name
    whitespace"""

UnexpectedCommaTest = verify_local_bear(
    ElmLintBear,
    valid_files=(good_file_no_unexpected_comma,),
    invalid_files=(bad_file_unexpected_comma,))

UnexpectedEndOfInputTest = verify_local_bear(
    ElmLintBear,
    valid_files=(good_file_no_unexpected_end_of_input,),
    invalid_files=(bad_file_unexpected_end_of_input,))

EmptyFileTest = verify_local_bear(
    ElmLintBear,
    valid_files=(good_file_not_empty,),
    invalid_files=(bad_file_empty,))

CommentTest = verify_local_bear(
    ElmLintBear,
    valid_files=(good_file_comment,),
    invalid_files=(bad_file_comment,))

ListTest = verify_local_bear(
    ElmLintBear,
    valid_files=(good_file_list,),
    invalid_files=(bad_file_list,))


@generate_skip_decorator(ElmLintBear)
class ElmLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = ElmLintBear(Section('name'), Queue())

    def test_bad_function(self):
        prepared = prepare_file(bad_file_function.splitlines(),
                                filename=None, create_tempfile=True)

        with prepared as (file, fname):
            self.check_results(
                self.uut,
                bad_file_function.splitlines(),
                [Result.from_values('ElmLintBear',
                                    message=result_message_bad_function,
                                    file=fname,
                                    line=6,
                                    severity=RESULT_SEVERITY.NORMAL)],
                filename=fname,
                create_tempfile=False)

    def test_good_function(self):
        prepared = prepare_file(good_file_function.splitlines(),
                                filename=None, create_tempfile=True)
        with prepared as (file, fname):
            self.check_results(
                self.uut,
                good_file_function.splitlines(),
                [],
                filename=fname,
                create_tempfile=False)
