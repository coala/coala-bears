import os
from queue import Queue

from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper

from bears.pug.PugLintBear import PugLintBear


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'puglint_test_files',
                        name)


def load_testfile(name):
    with open(get_testfile_path(name)) as f:
        return f.readlines()


@generate_skip_decorator(PugLintBear)
class PugLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = PugLintBear(Section('name'), Queue())

    def test_html_text(self):
        filename = 'html_text.pug'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PugLintBear',
                                message='HTML text must not be used',
                                file=get_testfile_path(filename),
                                line=1,
                                column=1,
                                end_line=1,
                                end_column=1,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename))

    def test_block_expansion(self):
        filename = 'block_expansion.pug'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PugLintBear',
                                message='Block expansion operators must not '
                                        'be used',
                                file=get_testfile_path(filename),
                                line=1,
                                column=2,
                                end_line=1,
                                end_column=2,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename))

    def test_class_attribute_with_static_value(self):
        filename = 'class_attribute_with_static_value.pug'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PugLintBear',
                                message='Static attribute "class" must be '
                                        'written as class literal',
                                file=get_testfile_path(filename),
                                line=1,
                                column=6,
                                end_line=1,
                                end_column=6,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename))

    def test_class_and_id_literals(self):
        filename = 'class_and_id_literals.pug'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PugLintBear',
                                message='Class literals must not be used',
                                file=get_testfile_path(filename),
                                line=1,
                                column=1,
                                end_line=1,
                                end_column=1,
                                severity=RESULT_SEVERITY.NORMAL),
             Result.from_values('PugLintBear',
                                message='ID literals must not be used',
                                file=get_testfile_path(filename),
                                line=2,
                                column=1,
                                end_line=2,
                                end_column=1,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename),
            settings={'prohibit_class_literals': True})

    def test_legacy_mixin_call(self):
        filename = 'legacy_mixin_call.pug'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PugLintBear',
                                message='Old mixin call syntax is not allowed',
                                file=get_testfile_path(filename),
                                line=1,
                                column=1,
                                end_line=1,
                                end_column=1,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename))

    def test_multiple_line_breaks(self):
        filename = 'multiple_line_breaks.pug'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PugLintBear',
                                message='Must not have multiple blank lines '
                                        'in a row',
                                file=get_testfile_path(filename),
                                line=3,
                                end_line=3,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename),
            settings={'prohibit_multiple_line_breaks': True})

    def test_spaces_inside_attribute_brackets(self):
        filename = 'spaces_inside_attribute_brackets.pug'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PugLintBear',
                                message='Illegal space after opening bracket',
                                file=get_testfile_path(filename),
                                line=1,
                                column=7,
                                end_line=1,
                                end_column=7,
                                severity=RESULT_SEVERITY.NORMAL),
             Result.from_values('PugLintBear',
                                message='Illegal space before closing bracket',
                                file=get_testfile_path(filename),
                                line=1,
                                column=46,
                                end_line=1,
                                end_column=46,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename))

    def test_preferred_quotation(self):
        filename = 'preferred_quotation.pug'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PugLintBear',
                                message='Invalid attribute quote mark found',
                                file=get_testfile_path(filename),
                                line=1,
                                column=31,
                                end_line=1,
                                end_column=31,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename))

    def test_config_file(self):
        filename = 'test_file.pug'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PugLintBear',
                                message='File must be at most 2 lines long',
                                file=get_testfile_path(filename),
                                line=6,
                                end_line=6,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename),
            settings={'puglint_config': get_testfile_path('.pug-lintrc')})
