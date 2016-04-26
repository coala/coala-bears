from bears.python.PyImportSortBear import PyImportSortBear
from tests.LocalBearTestHelper import verify_local_bear

PyImportSortBearTest = verify_local_bear(PyImportSortBear,
                                         (["import os\n", "import sys\n"],
                                          ("import os\n", "import sys\n")),
                                         (["import sys\n", "import os\n"],
                                          ("import sys\n", "import os\n")))

PyImportSortBearConfigsTest = verify_local_bear(
    PyImportSortBear,
    (("from os import read\n", "from sys import *\n"),),
    (("from os import read\n", "from os import *\n"),),
    settings={"combine_star_imports": True})

PyImportSortBearIgnoredConfigsTest = verify_local_bear(
    PyImportSortBear,
    (("import xyz\n", "\n", "import abc\n"),
     ("from xyz import *\n", "\n", "import abc\n")),
    (("import xyz\n", "import abc\n"),
     ("import abc\n", "import xyz\n")),
    settings={"known_standard_library_imports": "xyz",
              "known_first_party_imports": "abc"})
