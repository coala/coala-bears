from bears.swift.SwiftLintBear import SwiftLintBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """func swiftLintTest() {
	let someForceCast = NSNumber() as !Int
	let colonOnWrongSide: Int = 0
	// Smart enough to ignore comments in the code
	"let colonOnWrongSide : Int = 0" //
}
""".splitlines(True)

bad_file = """func swiftLintTest() {
\tlet someForceCast = NSNumber() as !Int
\tlet colonOnWrongSide : Int = 0
\t// Smart enough to ignore comments in the code
\t"let colonOnWrongSide : Int = 0" //
}""".splitlines(True)

SwiftLintBearTest = verify_local_bear(SwiftLintBear,
                                      valid_files=(good_file,),
                                      invalid_files=(bad_file,))