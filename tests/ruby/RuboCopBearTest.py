import os
from queue import Queue

from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper

from bears.ruby.RuboCopBear import RuboCopBear


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'test_files',
                        name)


def load_testfile(name):
    with open(get_testfile_path(name)) as f:
        return f.readlines()


@generate_skip_decorator(RuboCopBear)
class RuboCopBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = RuboCopBear(Section('name'), Queue())

    def test_good_file(self):
        filename = 'good_file.rb'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [],
            filename=get_testfile_path(filename))

    def test_bad_file(self):
        filename = 'bad_file.rb'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('RuboCopBear (Naming/MethodName)',
                                message='Use snake_case for method names.',
                                file=get_testfile_path(filename),
                                line=1,
                                column=5,
                                end_line=1,
                                end_column=12,
                                severity=RESULT_SEVERITY.INFO)],
            filename=get_testfile_path(filename))


# bad file becomes good and vice-versa
    def test_bad_config_file(self):
        filename = 'good_file.rb'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('RuboCopBear (Naming/MethodName)',
                                message='Use camelCase for method names.',
                                file=get_testfile_path(filename),
                                line=1,
                                column=5,
                                end_line=1,
                                end_column=14,
                                severity=RESULT_SEVERITY.INFO)],
            filename=get_testfile_path(filename),
            settings={'rubocop_config': get_testfile_path(
                'rubocop_config.yaml')})

    def test_good_config_file(self):
        filename = 'bad_file.rb'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [],
            filename=get_testfile_path(filename),
            settings={'rubocop_config': get_testfile_path(
                'rubocop_config.yaml')})

    def test_bad_indent_size(self):
        filename = 'indent_file.rb'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('RuboCopBear (Layout/CommentIndentation)',
                                message='Incorrect indentation detected '
                                        '(column 2 instead of 1).',
                                file=get_testfile_path(filename),
                                line=2,
                                column=3,
                                end_line=2,
                                end_column=20,
                                severity=RESULT_SEVERITY.INFO)],
            filename=get_testfile_path(filename),
            settings={'indent_size': 1})

    def test_good_indent_size(self):
        filename = 'indent_file.rb'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [],
            filename=get_testfile_path(filename))
