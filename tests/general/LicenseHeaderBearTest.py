import os
from queue import Queue

from bears.general.LicenseHeaderBear import LicenseHeaderBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.results.Result import Result
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'licenseheader_test_files',
                        name)


def load_testfile(name):
    with open(get_testfile_path(name)) as f:
        output = f.readlines()
    return output


class LicenseHeaderBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.uut = LicenseHeaderBear(self.section, Queue())

    def test_copyright_without_author(self):
        file_contents = load_testfile('CopyrightWithoutAuthor.java')
        self.check_validity(self.uut, file_contents)

    def test_copyright_with_given_author(self):
        file_contents = load_testfile('copyright_with_given_author.txt')
        self.section.append(Setting('author_name', 'The coala developers'))
        self.check_validity(
            self.uut,
            file_contents)

    def test_copyright_with_different_author(self):
        file_contents = load_testfile('copyright_with_different_author.txt')
        self.section.append(Setting('author_name', 'The coala developers'))
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('LicenseHeaderBear',
                                'Copyright notice with different/no author '
                                'present.',
                                file=get_testfile_path('copyright_with_diff'
                                                       'erent_author.txt'))],
            filename=get_testfile_path('copyright_with_'
                                       'different_author.txt'))

    def test_no_copyright(self):
        file_contents = load_testfile('no_copyright.py')
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('LicenseHeaderBear',
                                'Copyright notice not present.',
                                file=get_testfile_path('no_copyright.py'))],
            filename=get_testfile_path('no_copyright.py'))
