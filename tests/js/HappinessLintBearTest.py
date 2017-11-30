import re
from queue import Queue

from bears.js.HappinessLintBear import HappinessLintBear
from coalib.testing.LocalBearTestHelper import verify_local_bear
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator


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


@generate_skip_decorator(HappinessLintBear)
class HappinessLintBearConfigTest(LocalBearTestHelper):

    USE_SPACE_ERR_MSG = re.escape('"use_spaces=True" is incompatible with '
                                  'HappinessLintBear, set it to false.')

    def test_validate_use_spaces(self):
        section = Section('name')
        section.append(Setting('use_spaces', True))
        bear = HappinessLintBear(section, Queue())

        with self.assertRaisesRegex(ValueError, self.USE_SPACE_ERR_MSG):
            bear.run(bad_file, use_spaces=True)
