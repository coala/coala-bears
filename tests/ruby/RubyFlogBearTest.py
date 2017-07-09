import os
from queue import Queue

from bears.ruby.RubyFlogBear import RubyFlogBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'test_files/rubyflog_test_files',
                        name)


def load_testfile(name):
    with open(get_testfile_path(name)) as f:
        return f.readlines()


@generate_skip_decorator(RubyFlogBear)
class RubyFlogBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = RubyFlogBear(Section('name'), Queue())

    def test_good_flog_score(self):
        filename = 'test_good_flog_score.rb'
        file_contents = load_testfile(filename)

        expected_results = [Result.from_values('RubyFlogBear',
                                               message='Book:buy has a score of 2.3',
                                               file=get_testfile_path(
                                                   filename),
                                               line=2,
                                               end_line=5,
                                               severity=RESULT_SEVERITY.NORMAL)]

        self.check_results(
            self.uut,
            file_contents,
            expected_results,
            filename=get_testfile_path(filename))

    def test_moderate_flog_score(self):
        filename = 'test_moderate_flog_score.rb'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('RubyFlogBear',
                                message='The flog score of your method is '
                                        'moderate and might need refactoring',
                                file=get_testfile_path(filename),
                                line=2,
                                column=2,
                                end_line=19,
                                end_column=4,
                                severity=RESULT_SEVERITY.MAJOR)],
            filename=get_testfile_path(filename))

    def test_dangerous_flog_score(self):
        filename = 'test_dangerous_flog_score.rb'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('RubyFlogBear',
                                message='The flog score of your method is '
                                        'dangerously high and needs'
                                        ' refactoring',
                                file=get_testfile_path(filename),
                                line=2,
                                column=2,
                                end_line=23,
                                end_column=4,
                                severity=RESULT_SEVERITY.MAJOR)],
            filename=get_testfile_path(filename))
