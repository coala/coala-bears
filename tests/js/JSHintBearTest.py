from bears.js.JSHintBear import JSHintBear
from tests.LocalBearTestHelper import verify_local_bear
from coalib.misc.ContextManagers import prepare_file

test_file1 = """
var name = (function() { return 'Anton' }());
""".splitlines(keepends=True)


test_file2 = """
function () {
}()
""".splitlines(keepends=True)


config_file = """
{
  "lastsemic": true,
  "maxlen": 80
}
""".splitlines(keepends=True)


JSHintBearTest = verify_local_bear(JSHintBear,
                                   valid_files=(),
                                   invalid_files=(test_file1, test_file2))


with prepare_file(config_file,
                  filename=None,
                  force_linebreaks=True,
                  create_tempfile=True) as (conf_lines, conf_file):
    JSHintBearConfigFileTest = verify_local_bear(
        JSHintBear,
        valid_files=(test_file1, test_file2),
        invalid_files=(),
        settings={"jshint_config": conf_file})
