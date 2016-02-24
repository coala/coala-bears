from bears.general.LineLengthBear import LineLengthBear
from tests.LocalBearTestHelper import verify_local_bear

test_file = """
test
too
er
e
""".splitlines(keepends=True)


LineLengthBearTest = verify_local_bear(LineLengthBear,
                                       valid_files=(test_file,),
                                       invalid_files=(["testa"],
                                                      ["test line"]),
                                       settings={"max_line_length": "4"})


LineLengthBearIgnoreRegexTest = verify_local_bear(
    LineLengthBear,
    valid_files=(test_file,
                 ["http://a.domain.de"],
                 ["ftp://a.domain.de"],
                 ["hi there ftp://!"]),
    invalid_files=(["http not a link"],),
    settings={
        "max_line_length": "4",
        "ignore_length_regex": "http://, https://, ftp://"})
