from bears.dart.DartLintBear import DartLintBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
printNumber(num aNumber) {
  print('The number is $aNumber.');
}

main() {
  var answer = 42;          // The meaning of life.
  printNumber(answer);
}
""".splitlines(keepends=True)


bad_file = """
printNumber(num aNumber) {
  print('The number is $aNumber.')
}

main() {
  var answer = 42;          // The meaning of life.
  printNumber(answer)
}
""".splitlines(keepends=True)


DartLintBearTest = verify_local_bear(DartLintBear,
                                     valid_files=(good_file,),
                                     invalid_files=(bad_file,),
                                     tempfile_kwargs={"suffix": ".dart"})
