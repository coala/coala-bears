import os
from queue import Queue

from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator

from bears.yaml.TravisLintBear import TravisLintBear


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'travislint_test_files',
                        name)


def load_testfile(name):
    return open(get_testfile_path(name)).readlines()


@generate_skip_decorator(TravisLintBear)
class TravisLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = TravisLintBear(Section('name'), Queue())

    def test_good_file(self):
        file_name = '.good_travis.yml'
        file_contents = load_testfile(file_name)
        self.check_results(
            self.uut,
            file_contents,
            [],
            filename=get_testfile_path(file_name))

    def test_bad_file(self):
        file_name = '.bad_travis.yml'
        file_contents = load_testfile(file_name)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('TravisLintBear',
                                message='in matrix.exclude section: '
                                        'specified ruby, but setting is '
                                        'not relevant for python',
                                file=get_testfile_path(file_name),
                                severity=RESULT_SEVERITY.NORMAL),
             Result.from_values('TravisLintBear',
                                message='in os section: dropping osx, does'
                                        ' not support python',
                                file=get_testfile_path(file_name),
                                severity=RESULT_SEVERITY.NORMAL),
             Result.from_values('TravisLintBear',
                                message='specified ruby, but setting is '
                                        'not relevant for python',
                                file=get_testfile_path(file_name),
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(file_name))

    def test_empty_file(self):
        file_name = '.empty_travis.yml'
        file_contents = load_testfile(file_name)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('TravisLintBear',
                                message='missing key language, defaulting '
                                        'to ruby',
                                file=get_testfile_path(file_name),
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(file_name))
