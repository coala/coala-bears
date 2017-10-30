from bears.js.HappinessLintBear import HappinessLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


good_file = """
var x = 2;
if (x > 7) console.log('done');
console.log(x);
"""

bad_file = """
if (options.quiet !== true)
  console.log('done')
var x=2
"""

HappinessLintBearTest = verify_local_bear(HappinessLintBear,
                                          valid_files=(good_file,),
                                          invalid_files=(bad_file,))
