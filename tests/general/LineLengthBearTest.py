from bears.general.LineLengthBear import LineLengthBear
from coalib.testing.LocalBearTestHelper import verify_local_bear
from coalib.bearlib.aspects import (
    AspectList,
    get as get_aspect,
)

test_file = """
test
too
er
e
"""

invalid_general_file = 'C' * (79 + 1)

invalid_VB_file = 'C' * (65535 + 1)


LineLengthBearTest = verify_local_bear(LineLengthBear,
                                       valid_files=(test_file,),
                                       invalid_files=('testa',
                                                      'test line'),
                                       settings={'max_line_length': '4'})


LineLengthBearIgnoreRegexTest = verify_local_bear(
    LineLengthBear,
    valid_files=(test_file,
                 'http://a.domain.de',
                 'ftp://a.domain.de',
                 'hi there ftp://!'),
    invalid_files=('http not a link',),
    settings={
        'max_line_length': '4',
        'ignore_length_regex': 'http://, https://, ftp://'})


LineLengthBearLangSpecificLineLengthTest = verify_local_bear(
    LineLengthBear,
    valid_files=(test_file,),
    invalid_files=(invalid_VB_file,),
    settings={'language': 'VisualBasic'},
)


LineLengthBearValidLanguageTest = verify_local_bear(
    LineLengthBear,
    valid_files=(test_file,),
    invalid_files=(invalid_general_file,),
    settings={'language': 'C'},
)


LineLengthBearAspectTest = verify_local_bear(
    LineLengthBear,
    valid_files=(test_file,),
    invalid_files=('testa',
                   'test line'),
    aspects=AspectList([
        get_aspect('LineLength')('Unknown', max_line_length=4),
        ]),
)


SettingsOverAspectsPriorityTest = verify_local_bear(
    LineLengthBear,
    valid_files=(test_file,),
    invalid_files=('testa',
                   'test line'),
    aspects=AspectList([
        get_aspect('LineLength')('Unknown', max_line_length=10),
        ]),
    settings={'max_line_length': '4'},
)
