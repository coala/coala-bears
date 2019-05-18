from bears.natural_language.SpellCheckBear import SpellCheckBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

good_file = 'This is correct spelling.'

bad_file = 'tihs si surly som incoreclt speling.'


SpellCheckLintBearTest = verify_local_bear(SpellCheckBear,
                                           valid_files=(good_file,),
                                           invalid_files=(bad_file,))
