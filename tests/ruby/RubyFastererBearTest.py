import os
from queue import Queue

from coalib.results.Result import Result
from coalib.settings.Section import Section
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper

from bears.ruby.RubyFastererBear import RubyFastererBear


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'fasterer_test_files',
                        name)


def load_testfile(name):
    with open(get_testfile_path(name)) as f:
        return f.readlines()


@generate_skip_decorator(RubyFastererBear)
class RubyFastererBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = RubyFastererBear(Section('name'), Queue())

    def test_module_eval_vs_define_method(self):
        filename = 'module_eval.rb'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('RubyFastererBear',
                                message='Using module_eval is slower than '
                                        'define_method.',
                                file=get_testfile_path(filename),
                                line=3)],
            filename=get_testfile_path(filename))

    def test_sort_vs_sort_by(self):
        filename = 'sort_vs_sort_by.rb'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('RubyFastererBear',
                                message='Enumerable#sort is slower than '
                                        'Enumerable#sort_by.',
                                file=get_testfile_path(filename),
                                line=6)],
            filename=get_testfile_path(filename))
