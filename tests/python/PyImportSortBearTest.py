from queue import Queue

from bears.python.PyImportSortBear import PyImportSortBear
from tests.LocalBearTestHelper import LocalBearTestHelper, verify_local_bear
from coalib.results.Result import Result
from coalib.settings.Section import Section
from tests.python.ImportBearHelper import ImportBearHelper
PyImportSortBearTest = verify_local_bear(PyImportSortBear,
                                         ("import os\nimport sys\n",
                                          "import os\nimport sys\n"),
                                         ("import sys\nimport os\n",
                                          "import sys\nimport os\n"))

PyImportSortBearConfigsTest = verify_local_bear(
    PyImportSortBear,
    ("from os import read\nfrom sys import *\n",),
    ("from os import read\nfrom os import *\n",),
    settings={"combine_star_imports": True})

PyImportSortBearIgnoredConfigsTest = verify_local_bear(
    PyImportSortBear,
    ("import xyz\n\nimport abc\n",
     "from xyz import *\n\nimport abc\n"),
    ("import xyz\nimport abc\n",
     "import abc\nimport xyz\n"),
    settings={"known_standard_library_imports": "xyz",
              "known_first_party_imports": "abc"})


class PyImportSortBearTest(ImportBearHelper):

    def setUp(self):
        self.uut = PyImportSortBear(Section('name'), Queue())

    def test_run(self):
        file = "from abc import xyz, fgh"
        self.check_results(
            self.uut,
            ["from abc import xyz, fgh"],
            ["Imports fgh, xyz are sorted incorrectly."], file)
        self.check_results(
            self.uut,
            ["import z", "import g", "import e"],
            ["Imports e g are sorted incorrectly."], file)
