import os
from queue import Queue

from bears.general.LicenseCheckBear import LicenseCheckBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.results.Result import Result
from coalib.settings.Section import Section


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'licensecheck_test_files',
                        name)


def load_testfile(name):
    with open(get_testfile_path(name),'r') as file:
        output=file.readlines()
    return output



@generate_skip_decorator(LicenseCheckBear)
class LicenseCheckBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = LicenseCheckBear(Section('name'), Queue())

    def test_license(self):
        file_contents = load_testfile('mit_license.py')
        self.check_results(
            self.uut,
            file_contents,
            [],
            filename=get_testfile_path('mit_license.py'))

    def test_license_without_copyright(self):
        file_contents = load_testfile('apache_license_without_copyright.py')
        self.check_results(
            self.uut,
            file_contents,
            [],
            filename=get_testfile_path('apache_license_without_copyright.py'),
            settings={'licensecheck_lines': 70,
                      'licensecheck_tail': 0})

    def copyright_without_license(self):
        file_contents = load_testfile('copyright_without_license.py')
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('LicenseCheckBear',
                                'No license found.',
                                file=get_testfile_path('copyright_without_'
                                                       'license.py'))],
            filename=get_testfile_path('copyright_without_license.py'),
            settings={'licensecheck_lines': 0,
                      'licensecheck_tail': 0})  # Parse entire file

    def no_license(self):
        file_contents = load_testfile('no_license.py')
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('LicenseCheckBear',
                                'No license found.',
                                file=get_testfile_path('no_license.py'))],
            filename=get_testfile_path('no_license.py'),
            settings={'licensecheck_lines': 10})
