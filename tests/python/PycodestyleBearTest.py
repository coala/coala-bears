from bears.python.PycodestyleBear import PycodestyleBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


good_file = '''
def hello():
    print("hello world")
'''


bad_file = '''
import something



def hello():
    print("hello world")
'''

PycodestyleBearTest = verify_local_bear(
    PycodestyleBear,
    valid_files=(good_file,),
    invalid_files=(bad_file,))

PycodestyleBearNoIgnoreTest = verify_local_bear(
    PycodestyleBear,
    valid_files=(good_file,),
    invalid_files=(bad_file,),
    settings={'pycodestyle_ignore': ''})

PycodestyleBearConfigIgnoreTest = verify_local_bear(
    PycodestyleBear,
    valid_files=(good_file, bad_file),
    invalid_files=[],
    settings={'pycodestyle_ignore': 'E303'})

PycodestyleBearConfigSelectTest = verify_local_bear(
    PycodestyleBear,
    valid_files=(good_file, bad_file),
    invalid_files=[],
    settings={'pycodestyle_select': 'E300'})

long_line = 'a = "{0}"'.format('a' * 100)

PycodestyleBearLineLengthTest = verify_local_bear(
    PycodestyleBear,
    valid_files=(),
    invalid_files=(long_line,)
)

PycodestyleBearLineLengthTest = verify_local_bear(
    PycodestyleBear,
    valid_files=(long_line,),
    invalid_files=(),
    settings={'max_line_length': 200}
)

bad_file_2 = '''
x = "http://a.domain.de"




y = 5
'''

PycodestyleBearIgnoreRegexTest = verify_local_bear(
    PycodestyleBear,
    valid_files=('x = "ftps://a.domain.de"',
                 'x = "ftp://a.domain.de"',),
    invalid_files=(bad_file_2,),
    settings={'max_line_length': 5,
              'ignore_regex': 'ftps?://'}
)


PycodestyleBearDefaultRegexTest = verify_local_bear(
    PycodestyleBear,
    valid_files=('x = "http://a.domain.de"',
                 'x = "https://a.domain.de"',),
    invalid_files=('y = "htttps"',),
    settings={'max_line_length': 4}
)
