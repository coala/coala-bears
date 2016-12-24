from bears.java.InferBear import InferBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


good_file = """
class InferGood {
    int test() {
        String s = null;
        return s == null ? 0 : s.length();
    }
}
"""

bad_file = """
class InferBad {
    int test() {
        String s = null;
        return s.length();
    }
}
"""


InferBearTest = verify_local_bear(InferBear,
                                  valid_files=(good_file,),
                                  invalid_files=(bad_file,),
                                  tempfile_kwargs={'suffix': '.java'})
