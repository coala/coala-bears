import os

from bears.js.JSHintBear import JSHintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

test_file1 = """
var name = (function() { return 'Anton' }());
"""


test_file2 = """
function () {
}()
"""


test_file3 = """
var a = (function() {
  return 0;
}());
"""

# Test strictness and ES6
test_file4 = """
"use strict";

var foo = {
  bar: 1,
  baz: 2
};
var { bar, baz } = foo;
console.log(bar, baz);
"""


jshintconfig = os.path.join(os.path.dirname(__file__),
                            'test_files',
                            'jshintconfig.json')


settings = {
    'max_statements': 'False',
    'max_parameters': 10,
    'allow_unused_variables': 'True',
    'shadow': 'False',
    'allow_last_semicolon': 'True',
    'es_version': 3,
    'allow_latedef': 'no_func',
    'javascript_strictness': 'False'}


JSHintBearTest = verify_local_bear(JSHintBear,
                                   valid_files=(),
                                   invalid_files=(test_file1, test_file2,
                                                  test_file3))


JSHintBearConfigFileTest = verify_local_bear(
    JSHintBear,
    valid_files=(test_file1,),
    invalid_files=(test_file2,),
    settings={'jshint_config': jshintconfig})


JSHintBearCoafileTest = verify_local_bear(
    JSHintBear,
    invalid_files=(),
    valid_files=(test_file3, ),
    settings=settings)

JSHintBearDeprecationTest = verify_local_bear(
    JSHintBear,
    valid_files=(),
    invalid_files=(test_file4,),
    settings={'use_es6_syntax': 'False', 'allow_global_strict': 'False'})

JSHintBearDeprecation2Test = verify_local_bear(
    JSHintBear,
    valid_files=(test_file4,),
    invalid_files=(),
    settings={'use_es6_syntax': 'True', 'allow_global_strict': 'True'})
