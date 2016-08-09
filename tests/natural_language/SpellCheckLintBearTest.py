from bears.natural_language.SpellCheckLintBear import SpellCheckLintBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """This is correct spelling.
"""

bad_file = """tihs si surly som incoreclt speling.
"""


SpellCheckLintBearTest = verify_local_bear(SpellCheckLintBear,
                                           valid_files=(good_file,),
                                           invalid_files=(bad_file,))
