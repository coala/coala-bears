import os

from bears.go.GoMetaLintBear import GoMetaLintBear
from queue import Queue
from unittest.case import skipIf
from shutil import which

from coalib.testing.LocalBearTestHelper import execute_bear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


def get_test_file_path(testfile):
    return os.path.join(os.path.dirname(__file__),
                        'gometalinter_test_files',
                        testfile)


def load_test_file(filename):
    with open(get_test_file_path(filename)) as file:
        contents = file.read().splitlines(True)
    return contents


@skipIf(which('gometalinter') is None, 'gometalinter is not installed')
class GoMetaLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('')
        self.uut = GoMetaLintBear(self.section, Queue())
        self.bad_testfile1 = get_test_file_path('bad_testfile1.go')
        self.bad_testfile1_contents = load_test_file('bad_testfile1.go')
        self.bad_testfile2 = get_test_file_path('bad_testfile2.go')
        self.bad_testfile2_contents = load_test_file('bad_testfile2.go')
        self.good_testfile = get_test_file_path('good_testfile.go')
        self.config_file = get_test_file_path('test_config.json')
        self.maxDiff = None

    def test_validity(self):
        self.check_validity(self.uut, [], self.good_testfile)
        self.check_invalidity(self.uut, [], self.bad_testfile1)

    def test_mutually_exclusive_settings(self):
        self.section.append(Setting('enable_checks', 'golint,vet'))
        self.section.append(Setting('enable_all_checks', 'True'))
        with execute_bear(self.uut, 'bad_testfile2.go',
                          self.bad_testfile2_contents) as results:
            self.assertEqual(len(results), 0)

    def test_disable_all_and_enable(self):
        self.check_results(self.uut,
                           self.bad_testfile1_contents,
                           [Result.from_values(
                                   'GoMetaLintBear',
                                   message='undeclared name: fmt',
                                   file=self.bad_testfile1,
                                   line=4,
                                   column=4,
                                   additional_info='(gotype)',
                                   severity=RESULT_SEVERITY.MAJOR)],
                           filename=self.bad_testfile1,
                           settings={'disable_all_checks': True,
                                     'enable_checks': ['gotype']})

    def test_disable_all(self):
        self.section.append(Setting('disable_all_checks', 'True'))
        self.check_validity(self.uut, [], self.bad_testfile1)

    def test_enable(self):
        self.section.append(Setting('enable_checks', 'gotype,vet,structcheck'))
        self.check_invalidity(self.uut, [], self.bad_testfile2)

    def test_enable_all_and_disable(self):
        self.check_results(self.uut,
                           self.bad_testfile2_contents,
                           [],
                           filename=self.bad_testfile2,
                           settings={'enable_all_checks': True,
                                     'disable_checks': ['golint']})

    def test_enable_all(self):
        self.check_results(self.uut,
                           self.bad_testfile2_contents,
                           [Result.from_values(
                               'GoMetaLintBear',
                               message='should omit type int from '
                                       'declaration of var x; it '
                                       'will be inferred from the '
                                       'right-hand side',
                               file=self.bad_testfile2,
                               line=6,
                               column=10,
                               additional_info='(golint)',
                               severity=RESULT_SEVERITY.NORMAL)],
                           filename=self.bad_testfile2,
                           settings={'enable_all_checks': True})

    def test_disable(self):
        self.section.append(Setting('disable_checks', 'golint'))
        self.check_validity(self.uut, [], self.bad_testfile2)

    def test_config_file(self):
        self.section.append(
            Setting('gometalinter_config_file', 'test_config.json'))
        self.check_validity(self.uut, [], self.bad_testfile2)

    def test_ignore_config_file(self):
        self.section.append(Setting('gometalinter_config_file', 'False'))
        self.check_results(self.uut,
                           self.bad_testfile2_contents,
                           [],
                           filename=self.bad_testfile2,
                           settings={'disable_all_checks': True,
                                     'enable_checks': ['gotype', 'vet']})
