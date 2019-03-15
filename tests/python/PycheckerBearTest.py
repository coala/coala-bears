from queue import Queue
import os.path

from coalib.settings.Section import Section
from coalib.results.Result import Result
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator

from bears.python.PyCheckerBear import PyCheckerBear


def get_testfile_path(file):
    return os.path.join(os.path.dirname(__file__),
                        'pychecker_test_files', file)


def load_testfiles(name):
    with open(get_testfile_path(name)) as f1:
        contents = f1.read().splitlines(True)

    return contents


@generate_skip_decorator(PyCheckerBear)
class PyCheckerBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = PyCheckerBear(Section('name'), Queue())
        self.good_file = get_testfile_path('good_file.py')
        self.bad_file = get_testfile_path('bad_file.py')
        self.maxDiff = None

    def test_good_file(self):
        self.check_results(self.uut, load_testfiles('good_file.py'),
                           [],
                           self.good_file)

    def test_bad_file(self):
        self.check_results(self.uut, load_testfiles('bad_file.py'),
                           [Result.from_values('PyCheckerBear',
                                               'Parameter (c) not used',
                                               self.bad_file,
                                               line=1)],
                           self.bad_file)

    def test_cli_options(self):
        self.check_results(self.uut, load_testfiles('bad_file.py'),
                           [],
                           self.bad_file,
                           settings={'pychecker_cli_options': '--argsused=off'}
                           )
