import os

from bears.typescript.TSLintBear import TSLintBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """function findTitle(title) {
    let titleElement = "hello";
    return title;
}
let t = findTitle("mytitle");
t.innerHTML = "New title";
""".splitlines(True)

bad_file = """function findTitle(title) {
    let titleElement = 'hello';
    return title;
}
let t = findTitle('mytitle');
t.innerHTML = 'New title';
""".splitlines(True)

tslintconfig = os.path.join(os.path.dirname(__file__),
                            "test_files",
                            "tslint.json")

TSLintBearWithoutConfig = verify_local_bear(TSLintBear,
                                            valid_files=(good_file,),
                                            invalid_files=(bad_file,),
                                            tempfile_kwargs={"suffix": ".ts"})

TSLintBearTestWithConfig = verify_local_bear(TSLintBear,
                                             valid_files=(bad_file,),
                                             invalid_files=(good_file,),
                                             settings={"tslint_config":
                                                       tslintconfig},
                                             tempfile_kwargs={"suffix": ".ts"})

TSLintBearOtherOptions = verify_local_bear(TSLintBear,
                                           valid_files=(good_file,),
                                           invalid_files=(bad_file,),
                                           settings={"rules_dir": "/"},
                                           tempfile_kwargs={"suffix": ".ts"})
