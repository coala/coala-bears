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

PrettierLintBear = verify_local_bear(PrettierLintBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,))
