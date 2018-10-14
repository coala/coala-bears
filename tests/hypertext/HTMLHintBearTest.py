import os
from queue import Queue

from bears.hypertext.HTMLHintBear import HTMLHintBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Section import Section
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'htmlhint_test_files',
                        name)


def load_testfile(name):
    with open(get_testfile_path(name)) as f:
        return f.readlines()


@generate_skip_decorator(HTMLHintBear)
class HTMLHintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = HTMLHintBear(Section('name'), Queue())

    def test_bad_lowercase_tagname(self):
        filename = 'test_bad_lowercase_tagname.html'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('HTMLHintBear',
                                message='The html element name of [ SPAN ] '
                                        'must be in lowercase.',
                                file=get_testfile_path(filename),
                                line=2,
                                column=1,
                                end_line=2,
                                end_column=1,
                                severity=RESULT_SEVERITY.MAJOR),
             Result.from_values('HTMLHintBear',
                                message='The html element name of [ SPAN ] '
                                        'must be in lowercase.',
                                file=get_testfile_path(filename),
                                line=3,
                                column=1,
                                end_line=3,
                                end_column=1,
                                severity=RESULT_SEVERITY.MAJOR)],
            filename=get_testfile_path(filename))

    def test_bad_lowercase_attribute(self):
        filename = 'test_bad_lowercase_attribute.html'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('HTMLHintBear',
                                message='The attribute name of [ TYPE ] must '
                                        'be in lowercase.',
                                file=get_testfile_path(filename),
                                line=2,
                                column=7,
                                end_line=2,
                                end_column=7,
                                severity=RESULT_SEVERITY.MAJOR)],
            filename=get_testfile_path(filename))

    def test_attribute_duplication(self):
        filename = 'test_attribute_duplication.html'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('HTMLHintBear',
                                message='Duplicate of attribute name [ type ] '
                                        'was found.',
                                file=get_testfile_path(filename),
                                line=2,
                                column=36,
                                end_line=2,
                                end_column=36,
                                severity=RESULT_SEVERITY.MAJOR)],
            filename=get_testfile_path(filename))

    def test_bad_tag_pair(self):
        filename = 'test_bad_tag_pair.html'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('HTMLHintBear',
                                message='Tag must be paired, missing: '
                                        '[ </li> ], start tag match failed '
                                        '[ <li> ] on line 2.',
                                file=get_testfile_path(filename),
                                line=2,
                                column=9,
                                end_line=2,
                                end_column=9,
                                severity=RESULT_SEVERITY.MAJOR)],
            filename=get_testfile_path(filename))

    def test_doctype_at_beginning(self):
        filename = 'test_doctype_at_beginning.html'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('HTMLHintBear',
                                message='Doctype must be declared first.',
                                file=get_testfile_path(filename),
                                line=1,
                                column=1,
                                end_line=1,
                                end_column=1,
                                severity=RESULT_SEVERITY.MAJOR)],
            filename=get_testfile_path(filename))

    def test_bad_unique_attribute_id(self):
        filename = 'test_bad_unique_attribute_id.html'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('HTMLHintBear',
                                message='The id value [ id1 ] must be unique.',
                                file=get_testfile_path(filename),
                                line=2,
                                column=25,
                                end_line=2,
                                end_column=25,
                                severity=RESULT_SEVERITY.MAJOR)],
            filename=get_testfile_path(filename))

    def test_require_alt_attribute(self):
        filename = 'test_require_alt_attribute.html'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('HTMLHintBear',
                                message='An alt attribute must be present on '
                                        '<img> elements.',
                                file=get_testfile_path(filename),
                                line=2,
                                column=5,
                                end_line=2,
                                end_column=5,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename))

    def test_config_file(self):
        filename = 'test_bad_inline_style.html'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('HTMLHintBear',
                                message='Inline style [  style="color:red" ] '
                                        'cannot be use.',
                                file=get_testfile_path(filename),
                                line=2,
                                column=5,
                                end_line=2,
                                end_column=5,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename),
            settings={'htmlhint_config': get_testfile_path('.htmlhintrc')})

    def test_absolute_links_in_href(self):
        filename = 'test_links_in_href.html'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('HTMLHintBear',
                                message='The value of the href attribute '
                                        '[ test.html ] must be absolute.',
                                file=get_testfile_path(filename),
                                line=2,
                                column=3,
                                end_line=2,
                                end_column=3,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename),
            settings={'require_relative_links_in_href': False})

    def test_relative_links_in_href(self):
        filename = 'test_links_in_href.html'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('HTMLHintBear',
                                message='The value of the href attribute '
                                        '[ http://www.alibaba.com/ ] must be '
                                        'relative.',
                                file=get_testfile_path(filename),
                                line=3,
                                column=3,
                                end_line=3,
                                end_column=3,
                                severity=RESULT_SEVERITY.NORMAL)],
            filename=get_testfile_path(filename),
            settings={'require_relative_links_in_href': True})
