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

with_unused_variables = """
def main():
    x = 10
    y = 11
    print(y)
"""

without_unused_variables = """
def main():
    y = 11
    print(y)
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

PyUnusedVariablesTest = verify_local_bear(
                PyUnusedCodeBear,
                valid_files=[without_unused_variables],
                invalid_files=[with_unused_variables],
                settings={'remove_unused_variables': True})

PyUnusedVariablesBearTest = verify_local_bear(
                PyUnusedCodeBear,
                valid_files=[with_unused_variables],
                invalid_files=[],
                settings={'remove_unused_variables': False})
