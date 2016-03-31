import os

from bears.js.ESLintBear import ESLintBear
from tests.LocalBearTestHelper import verify_local_bear


test_good = """function addOne(i) {
    if (!isNaN(i)) {
        return i+1;
    }
    return i;
}

addOne(3);
""".splitlines(True)

test_bad = """function addOne(i) {
    if (i != NaN) {
        return i ++
    }
    else {
        return
    }
};
""".splitlines(True)

eslintconfig = os.path.join(os.path.dirname(__file__),
                            "test_files",
                            "eslintconfig.json")

ESLintBearTestWithConfig = verify_local_bear(ESLintBear,
                                             valid_files=(test_good,),
                                             invalid_files=(test_bad,),
                                             settings={"eslint_config":
                                                       eslintconfig})

ESLintBearWithoutConfig = verify_local_bear(ESLintBear,
                                            valid_files=(test_good, test_bad),
                                            invalid_files=())
