import os
from queue import Queue

from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper

from bears.hypertext.HTTPoliceLintBear import HTTPoliceLintBear


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'httpolice_test_files',
                        name)


def load_testfile(name):
    with open(get_testfile_path(name)) as f:
        return f.readlines()


@generate_skip_decorator(HTTPoliceLintBear)
class HTTPoliceLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = HTTPoliceLintBear(Section('name'), Queue())

    def test_syntax_error_in_request_target(self):
        filename = 'test_syntax_error_in_request_target.har'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('HTTPoliceLintBear',
                                message='1045 Syntax error in request target',
                                file=get_testfile_path(filename),
                                severity=RESULT_SEVERITY.MAJOR)],
            filename=get_testfile_path(filename))

    def test_bad_header(self):
        filename = 'test_bad_header.har'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('HTTPoliceLintBear',
                                message="1244 TE header can't be used in "
                                        'HTTP/2',
                                file=get_testfile_path(filename),
                                severity=RESULT_SEVERITY.MAJOR)],
            filename=get_testfile_path(filename))

    def test_silence_id_setting(self):
        filename = 'test_bad_header.har'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [],
            filename=get_testfile_path(filename),
            settings={'httpolice_silence_ids': ['1244']})

    def test_good_file(self):
        filename = 'test_valid_file.har'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [],
            filename=get_testfile_path(filename))
