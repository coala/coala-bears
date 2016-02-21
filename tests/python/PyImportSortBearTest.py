from bears.python.PyImportSortBear import PyImportSortBear
from tests.LocalBearTestHelper import verify_local_bear

PyImportSortBearTest = verify_local_bear(PyImportSortBear,
                                         (["import os\n", "import sys\n"],
                                          ("import os\n", "import sys\n")),
                                         (["import sys\n", "import os\n"],
                                          ("import sys\n", "import os\n")))
