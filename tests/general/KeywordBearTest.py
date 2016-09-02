from bears.general.KeywordBear import KeywordBear
from tests.LocalBearTestHelper import verify_local_bear

test_file = """
test line fix me
to do
error fixme
"""


KeywordBearTest = verify_local_bear(
    KeywordBear,
    valid_files=(test_file,),
    invalid_files=("test line FIXME",
                   "test line todo",
                   "test line warNING",
                   "test line ERROR"),
    settings={
       "keywords_case_sensitive": "FIXME, ERROR",
       "keywords_case_insensitive": "todo, warning"
    })
