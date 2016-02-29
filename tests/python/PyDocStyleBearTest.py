from bears.python.PyDocStyleBear import PyDocStyleBear
from tests.LocalBearTestHelper import verify_local_bear


good_file = '''
"""example module level docstring."""


def hello():
    """Print hello world."""
    print("hello world")

'''.splitlines(keepends=True)


bad_file = '''
"""
example module level docstring
"""

def hello():
    print("hello world")

'''.splitlines(keepends=True)

PyDocStyleBearTest = verify_local_bear(PyDocStyleBear,
                                       valid_files=(good_file,),
                                       invalid_files=(bad_file,),
                                       tempfile_kwargs={"suffix": ".py"})
