import platform
import unittest

from bears.natural_language.SpellCheckBear import SpellCheckBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = 'This is correct spelling.'

bad_file = 'tihs si surly som incoreclt speling.'


SpellCheckLintBearTest = unittest.skipIf(
    platform.system() == 'Windows',
    "SpellCheckBear doesn't work on windows")(
        verify_local_bear(SpellCheckBear,
                          valid_files=(good_file,),
                          invalid_files=(bad_file,)))
