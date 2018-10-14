from bears.matlab.MatlabIndentationBear import MatlabIndentationBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

MatlabIndentationBearTest = verify_local_bear(
    MatlabIndentationBear,
    valid_files=('if a ~= b\n  a\nendif\n',
                 'if a ~= b\n  a\nendif\n',
                 'if a ~= b\n  a\n  \nelse\n  a\nendif\n'),
    invalid_files=('  A',
                   'if a ~= b\na\nendif\n',
                   'if a ~= b\n a\nendif\n',
                   'if a ~= b\n a\nendif\n',
                   'if a ~= b\n  a\n  else\n  a\nendif\n'))
