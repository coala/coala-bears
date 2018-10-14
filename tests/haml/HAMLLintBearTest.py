import os
from queue import Queue

from coalib.settings.Section import Section
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator

from bears.haml.HAMLLintBear import HAMLLintBear


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'hamllint_test_files',
                        name)


def load_testfile(name):
    with open(get_testfile_path(name)) as f:
        return f.readlines()


@generate_skip_decorator(HAMLLintBear)
class HAMLLintBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.uut = HAMLLintBear(self.section, Queue())

    def test_alignment_tabs(self):
        good_filename = 'test_alignment_tabs_good_file.haml'
        file_contents = load_testfile(good_filename)
        self.check_validity(self.uut, file_contents)

    def test_alt_text(self):
        good_filename = 'test_alt_text_good_file.haml'
        file_contents = load_testfile(good_filename)
        self.check_validity(self.uut, file_contents)

        bad_filename = 'test_alt_text_bad_file.haml'
        file_contents = load_testfile(bad_filename)
        self.check_invalidity(self.uut, file_contents)

    def test_class_attribute_with_static_value(self):
        good_file = ['%tag.my-class']
        self.check_validity(self.uut, good_file)

        bad_file = ['%tag{ ',
                    'class: ',
                    '\'my-class'
                    '\' }']
        self.check_invalidity(self.uut, bad_file)

    def test_classes_before_ids(self):
        good_file = ['%tag.class#id']
        self.check_validity(self.uut, good_file)

        bad_file = ['%tag#id.class']
        self.check_invalidity(self.uut, bad_file)

    def test_config_file(self):
        filename = 'test_no_trailing_whitespace_file.haml'
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [],
            filename=get_testfile_path(filename),
            settings={'hamllint_config': get_testfile_path('.haml-lint.yml')})

    def test_consecutive_comments(self):
        good_filename = 'test_consecutive_comments_good_file.haml'
        file_contents = load_testfile(good_filename)
        self.check_validity(self.uut, file_contents)

        bad_filename = 'test_consecutive_comments_bad_file.haml'
        file_contents = load_testfile(bad_filename)
        self.check_invalidity(self.uut, file_contents)

        good_filename = 'test_consecutive_comments_good_file_via_config.haml'
        file_contents = load_testfile(good_filename)
        settings = {'max_consecutive_comments': 2}
        self.check_validity(self.uut, file_contents, settings=settings)

    def test_consecutive_silent_scripts(self):
        good_filename = 'test_consecutive_silent_scripts_good_file.haml'
        file_contents = load_testfile(good_filename)
        self.check_validity(self.uut, file_contents)

        bad_filename = 'test_consecutive_silent_scripts_bad_file.haml'
        file_contents = load_testfile(bad_filename)
        self.check_invalidity(self.uut, file_contents)

    def test_empty_object_reference(self):
        good_file = ['%tag']
        self.check_validity(self.uut, good_file)

        bad_file = ['%tag[]']
        self.check_invalidity(self.uut, bad_file)

    def test_empty_script(self):
        good_file = ['- some_expression']
        self.check_validity(self.uut, good_file)

        bad_file = ['-']
        self.check_invalidity(self.uut, bad_file)

    def test_final_newline(self):
        bad_filename = 'test_no_trailing_whitespace_file.haml'
        file_contents = load_testfile(bad_filename)
        self.check_invalidity(self.uut, file_contents)

    def test_html_attributes(self):
        good_file = ['%tag{ lang: \'en\' }']
        self.check_validity(self.uut, good_file)

        bad_file = ['%tag(lang=en)']
        self.check_invalidity(self.uut, bad_file)

    def test_inline_styles(self):
        good_file = ['%p.warning']
        self.check_validity(self.uut, good_file)

        bad_file = ['%p{ style: \'color: red;\' }']
        self.check_invalidity(self.uut, bad_file)

    def test_syntax(self):
        good_file = ['%div\n',
                     '%p Hello, world']
        self.check_validity(self.uut, good_file)

        bad_file = ['%div\n',
                    '% Hello, world']
        self.check_invalidity(self.uut, bad_file)
