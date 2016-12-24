from bears.python.PyUnusedCodeBear import PyUnusedCodeBear
from coalib.testing.LocalBearTestHelper import verify_local_bear


invalid_imports = """
import sys
import os
import mymodule
print("Hello World")
"""

valid_import = """
import sys
sys.exit()
"""

invalid_from_import = """
import sys
from os import name
sys.exit()
import re
"""
valid_from_import = """
from sys import exit
form os import name

print(name)
exit()
"""

valid_non_builtin = """
import mymodule
import sys
sys.exit(0)
"""

PyAllUnusedImportTest = verify_local_bear(
                PyUnusedCodeBear,
                valid_files=[valid_import,
                             valid_from_import],
                invalid_files=[invalid_imports,
                               invalid_from_import,
                               valid_non_builtin
                               ],
                settings={'remove_all_unused_imports': True})

PyUnusedCodeBearTest = verify_local_bear(
                PyUnusedCodeBear,
                valid_files=[valid_non_builtin,
                             valid_import,
                             valid_from_import],
                invalid_files=[invalid_imports,
                               invalid_from_import],
                settings={'remove_all_unused_imports': False})
