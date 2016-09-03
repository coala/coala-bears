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
    invalid_files=("test line todo",
                   "test line warNING"),
    settings={"keywords": "todo, warning"})
