from bears.java.InferBear import InferBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
class InferGood {
    int test() {
        String s = null;
        return s == null ? 0 : s.length();
    }
}
""".splitlines(keepends=True)

bad_file = """
class InferBad {
    int test() {
        String s = null;
        return s.length();
    }
}
""".splitlines(keepends=True)


InferBearTest = verify_local_bear(InferBear,
                                  valid_files=(good_file,),
                                  invalid_files=(bad_file,),
                                  tempfile_kwargs={"suffix": ".java"})
