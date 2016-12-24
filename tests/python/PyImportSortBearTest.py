from bears.python.PyImportSortBear import PyImportSortBear
from coalib.testing.LocalBearTestHelper import verify_local_bear

PyImportSortBearTest = verify_local_bear(PyImportSortBear,
                                         ('import os\nimport sys\n',
                                          'import os\nimport sys\n'),
                                         ('import sys\nimport os\n',
                                          'import sys\nimport os\n'))

PyImportSortBearConfigsTest = verify_local_bear(
    PyImportSortBear,
    ('from os import read\nfrom sys import *\n',),
    ('from os import read\nfrom os import *\n',),
    settings={'combine_star_imports': True})

PyImportSortBearIgnoredConfigsTest = verify_local_bear(
    PyImportSortBear,
    ('import xyz\n\nimport abc\n',
     'from xyz import *\n\nimport abc\n'),
    ('import xyz\nimport abc\n',
     'import abc\nimport xyz\n'),
    settings={'known_standard_library_imports': 'xyz',
              'known_first_party_imports': 'abc'})
