from bears.python.PyImportSortBear import PyImportSortBear
from coalib.testing.LocalBearTestHelper import verify_local_bear
import unittest
from queue import Queue

from coalib.settings.Section import Section

from coalib.results.Diff import Diff

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

PyImportSortBearThirdPartyConfigTest = verify_local_bear(
    PyImportSortBear,
    ('import sys\n\nimport datetime\n',),
    ('import datetime\nimport sys\n',),
    settings={'known_third_party_imports': 'datetime'})


class PyImportSortBearTest(unittest.TestCase):

    def setUp(self):
        self.queue = Queue()
        self.section = Section('PyImportSortBear')
        self.uut = PyImportSortBear(self.section,
                                    self.queue)

    def test_isort_settings(self):
        test_file = """
import os
import re

import requests
""".splitlines(True)

        test_file2 = """
import re
import os

import requests
""".splitlines(True)

        self.assertEqual(list(self.uut.run('', test_file)), [])
        self.assertEqual(list(self.uut.run('',
                                           test_file2))[0].diffs[''].modified,
                         ['\n', 'import os\n', 'import re\n', '\n',
                          'import requests\n'])

    def test_treat_seperated_imports_independently(self):
        test_file = (
            """
import re
import requests
from urllib.parse import urlparse

from coalib.results.Diff import Diff
from coalib.bears.LocalBear import LocalBear
""".splitlines(True)
        )

        expected = (
            """
import re
from urllib.parse import urlparse

import requests

from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
""".splitlines(True)
        )
        diff = Diff(expected)
        settings = {'treat_seperated_imports_independently': True}
        self.assertEqual(list(self.uut.run('',
                                           test_file,
                                           **settings))[0].diffs[''].modified,
                         diff.modified)

        self.assertEqual(list(self.uut.run('',
                                           ['import curses\n', 'import io\n',
                                            'coala = "coala"\n'],
                                           **settings)), [])

    def test_import_seperation(self):
        file = (
            """
from x import (y,
               z,
               w)
import this

import a, b
""".splitlines(True)
        )
        seperated = [[(2, 'from x import (y,\n'),
                      (3, '               z,\n'),
                      (4, '               w)\n'),
                      (5, 'import this\n')],
                     [(7, 'import a, b\n')]]

        self.assertEqual(self.uut._seperate_imports(file),
                         seperated)
