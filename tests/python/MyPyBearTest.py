from bears.python.MyPyBear import MyPyBear
from tests.LocalBearTestHelper import verify_local_bear

good_file = """
import typing
def greet(name: str) -> None:
    print('Hello', name)
greet('Jack')
"""

bad_file = """
import typing
def greet(name: int) -> None:
    print('Hello', name)
greet('Jack')
"""

MyPyBearTest = verify_local_bear(MyPyBear,
                                 valid_files=(good_file,),
                                 invalid_files=(bad_file,),)
