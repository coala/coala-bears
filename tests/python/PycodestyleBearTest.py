from bears.python.PycodestyleBear import PycodestyleBear
from tests.LocalBearTestHelper import verify_local_bear


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