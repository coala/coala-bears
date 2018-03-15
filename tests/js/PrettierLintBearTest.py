from bears.js.PrettierLintBear import PrettierLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """foo(
  reallyLongArg(),
  omgSoManyParameters(),
  IShouldRefactorThis(),
  isThereSeriouslyAnotherOne()
);"""

# Start ignoring PycodestyleBear, LineLengthBear
bad_file = """
foo(reallyLongArg(), omgSoManyParameters(), IShouldRefactorThis(), isThereSeriouslyAnotherOne());
"""
# Stop ignoring

bad_semicolon = """
var x;
"""

good_quotes = """const a = () => "Foo bar";

function b(object, key) {
  return object["key"];
}"""

bad_quotes = """const a = () => 'Foo bar';"""

bad_parentheses = """function b(){
"""

good_parentheses = """function b() {}
"""

bad_indent = """if (x) {
x = 0
}"""

good_indent = """if (x) {
  x = 0;
}"""

PrettierLintBear = verify_local_bear(PrettierLintBear,
                                     valid_files=(good_quotes,
                                                  good_file,
                                                  good_parentheses,
                                                  good_indent,),
                                     invalid_files=(bad_file,
                                                    bad_quotes,
                                                    bad_parentheses,
                                                    bad_indent,))
