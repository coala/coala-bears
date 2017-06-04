import os
from queue import Queue

from bears.stylus.StylintBear import StylintBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'stylint_test_files',
                        name)


def load_testfile(name):
    with open(get_testfile_path(name)) as f:
        return f.readlines()


@generate_skip_decorator(StylintBear)
class StylintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = StylintBear(Section('name'), Queue())

    def test_bad_missing_colon(self):
        filename = 'test_bad_missing_colon.styl'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('StylintBear',
                                message='missing colon between property '
                                        'and value',
                                file=get_testfile_path(filename),
                                line=2,
                                column=6,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename))

    def test_bad_duplicates(self):
        filename = 'test_bad_duplicates.styl'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('StylintBear',
                                message='duplicate property or selector, '
                                        'consider merging',
                                file=get_testfile_path(filename),
                                line=4,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename))

    def test_bad_no_important(self):
        filename = 'test_bad_no_important.styl'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('StylintBear',
                                message='!important is disallowed',
                                file=get_testfile_path(filename),
                                line=2,
                                column=9,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename))

    def test_bad_brackets(self):
        filename = 'test_bad_brackets.styl'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('StylintBear',
                                message='unnecessary bracket',
                                file=get_testfile_path(filename),
                                line=1,
                                column=13,
                                severity=RESULT_SEVERITY.NORMAL),
             Result.from_values('StylintBear',
                                message='unnecessary bracket',
                                file=get_testfile_path(filename),
                                line=3,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename))

    def test_bad_semicolon(self):
        filename = 'test_bad_semicolon.styl'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('StylintBear',
                                message='unnecessary semicolon found',
                                file=get_testfile_path(filename),
                                line=2,
                                column=19,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename))

    def test_bad_alphabetical_order(self):
        filename = 'test_bad_alphabetical_order.styl'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('StylintBear',
                                message='prefer alphabetical when sorting '
                                        'properties',
                                file=get_testfile_path(filename),
                                line=3,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename))

    def test_bad_trailing_whitespace(self):
        filename = 'test_bad_trailing_whitespace.styl'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('StylintBear',
                                message='trailing whitespace',
                                file=get_testfile_path(filename),
                                line=3,
                                column=22,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename))

    def test_bad_mixed_spaces_tabs(self):
        filename = 'test_bad_mixed_spaces_tabs.styl'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('StylintBear',
                                message='mixed spaces and tabs',
                                file=get_testfile_path(filename),
                                line=3,
                                column=0,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename),
            settings={'stylint_config': get_testfile_path('.stylintrc')})

    def test_bad_placeholder_space_color(self):
        filename = 'test_bad_placeholder_space_color.styl'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('StylintBear',
                                message='always use a placeholder variable '
                                        'when extending',
                                file=get_testfile_path(filename),
                                line=4,
                                severity=RESULT_SEVERITY.NORMAL),
             Result.from_values('StylintBear',
                                message='hexidecimal color should '
                                        'be a variable',
                                file=get_testfile_path(filename),
                                line=6,
                                column=8,
                                severity=RESULT_SEVERITY.NORMAL),
             Result.from_values('StylintBear',
                                message='line comments require a space '
                                        'after //',
                                file=get_testfile_path(filename),
                                line=8,
                                column=2,
                                severity=RESULT_SEVERITY.NORMAL),
             Result.from_values('StylintBear',
                                message='commas must be followed '
                                        'by a space for readability',
                                file=get_testfile_path(filename),
                                line=9,
                                column=6,
                                severity=RESULT_SEVERITY.NORMAL),
             ],
            filename=get_testfile_path(filename))

    def test_valid_file(self):
        filename = 'test_valid_file.styl'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [],
            filename=get_testfile_path(filename))
