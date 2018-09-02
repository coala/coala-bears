import os

from bears.typescript.TSLintBear import TSLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = """function findTitle(title) {
    let titleElement = "hello";
    return title;
}
let t = findTitle("mytitle");
t.innerHTML = "New title";
"""

bad_file = """function findTitle(title) {
    let titleElement = 'hello';
    return title;
}
let t = findTitle('mytitle');
t.innerHTML = 'New title';
"""

tslint_config_dir = os.path.join(os.path.dirname(__file__), 'test_files')

tslintconfig = os.path.join(tslint_config_dir,
                            'tslint.json')

tslintconfig_single = os.path.join(tslint_config_dir,
                                   'tslint-single.json')

TSLintDoubleQuotesTest = verify_local_bear(
    TSLintBear,
    valid_files=(good_file,),
    invalid_files=(bad_file,),
    settings={
        'tslint_config': tslintconfig,
        'rules_dir': tslint_config_dir,
    },
    tempfile_kwargs={'suffix': '.ts'})

TSLintSingleQuotesTest = verify_local_bear(
    TSLintBear,
    valid_files=(bad_file,),
    invalid_files=(good_file,),
    settings={'tslint_config': tslintconfig_single},
    tempfile_kwargs={'suffix': '.ts'})
