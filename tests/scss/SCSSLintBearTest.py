from bears.scss.SCSSLintBear import SCSSLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


good_file = """
.btn-primary {
  &:hover {
    background-color: darken($btn-primary-bg, 3%);
  }
}
"""

bad_file = """
.btn-primary {
  &:hover {
    background-color: darken($btn-primary-bg, 3%)
}
"""

bad_file2 = '''
$value: 5px;

 .foo {
  padding: $value;
}

.bar {
  margin: $value;
}

.foo.bar {
  display: block;
}
'''

good_file2 = '''
$value: 5px;

.foo {
  padding: $value;
}

.bar {
  margin: $value;
}

.new-class {
  display: block;
}
'''


SCSSLintBearTest = verify_local_bear(SCSSLintBear,
                                     valid_files=(good_file, good_file2),
                                     invalid_files=(bad_file, bad_file2))


SCSSLintBearChainedClassesTest = verify_local_bear(
    SCSSLintBear,
    valid_files=(good_file, good_file2),
    invalid_files=(bad_file, bad_file2),
    settings={'allow_chained_classes': True})
