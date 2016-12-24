import os

from bears.js.ESLintBear import ESLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


test_good = """function addOne(i) {
    if (!isNaN(i)) {
        return i+1;
    }
    return i;
}

addOne(3);
"""

test_bad = """function addOne(i) {
    if (i != NaN) {
        return i ++
    }
    else {
        return
    }
};
"""

test_import_good = """
import test from "./test";

test();
"""

test_import_bad = """
import test from "../test";

test();
"""

test_syntax_error = '{<!@3@^ yeah!/\n'

test_dir = os.path.join(os.path.dirname(__file__), 'test_files')

ESLintBearWithConfigTest = verify_local_bear(
    ESLintBear,
    valid_files=('',),
    invalid_files=(test_bad, test_good),
    settings={'eslint_config': os.path.join(test_dir, 'eslintconfig.json')})

ESLintBearWithoutConfigTest = verify_local_bear(
    ESLintBear,
    valid_files=(test_good, ''),
    invalid_files=(test_syntax_error, test_bad))

# If there is an invalid config file, the results cannot be found. So, no
# file gives a result.
ESLintBearWithUnloadablePluginTest = verify_local_bear(
    ESLintBear,
    valid_files=(test_bad, test_good),
    invalid_files=(),
    settings={'eslint_config': os.path.join(test_dir,
                                            'eslintconfig_badplugin.json')})
ESLintBearImportTest = verify_local_bear(
    ESLintBear,
    valid_files=(test_import_good, ),
    invalid_files=(test_import_bad, ),
    filename=os.path.join(test_dir, 'test.js'),
    create_tempfile=False,
    settings={'eslint_config': os.path.join(test_dir,
                                            'eslintconfig_import.json')})
