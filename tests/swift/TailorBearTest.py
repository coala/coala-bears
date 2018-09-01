import os

from bears.swift.TailorBear import TailorBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

tailorconfig = os.path.join(os.path.dirname(__file__),
                            'test_files',
                            'tailor.yaml')

good_file = """class UpperCamelCase {
  var x: Int
}
"""

bad_file = """class lowerCamelCase {
  var x: Int
}
"""

long_class_file = """class LongClass {
  var x: Int
  var y: Int
  var z: Int
}
"""

TailorBearWithoutConfigTest = verify_local_bear(
    TailorBear,
    valid_files=(good_file,),
    invalid_files=(bad_file,),
    tempfile_kwargs={'suffix': '.swift'})

TailorBearWithConfigTest = verify_local_bear(
    TailorBear,
    valid_files=(bad_file,),
    invalid_files=(),
    settings={'tailor_config': tailorconfig},
    tempfile_kwargs={'suffix': '.swift'})

TailorBearWithSettingTest = verify_local_bear(
    TailorBear,
    valid_files=(),
    invalid_files=(long_class_file,),
    settings={'max_class_length': 2},
    tempfile_kwargs={'suffix': '.swift'})
