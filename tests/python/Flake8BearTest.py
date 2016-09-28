from bears.python.Flake8Bear import Flake8Bear
from tests.LocalBearTestHelper import verify_local_bear


good_file = """
message = 'HelloWorld'
print(message)
"""

bad_file = """
import os
message ='HelloWorld'
print(message)
"""

Flake8Bear = verify_local_bear(Flake8Bear,
                               valid_files=(good_file, bad_file),
                               invalid_files=())
