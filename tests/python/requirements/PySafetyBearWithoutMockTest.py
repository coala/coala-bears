import os

from queue import Queue
from bears.python.requirements.PySafetyBear import PySafetyBear
from coalib.settings.Section import Section
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.testing.BearTestHelper import generate_skip_decorator


def get_testfile_path(name):
    return os.path.join(os.path.dirname(__file__),
                        'PySafety_test_files',
                        name)


def load_testfile(name):
    return open(get_testfile_path(name)).readlines()


@generate_skip_decorator(PySafetyBear)
class PySafetyBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = PySafetyBear(Section('name'), Queue())

    def test_without_vulnerability(self):
        self.check_validity(self.uut, ['lxml==3.6.0'])

    def test_with_vulnerability(self):
        self.check_invalidity(self.uut, ['bottle==0.10.1'])

    def test_with_cve_vulnerability(self):
        file_name = 'requirement.txt'
        file_contents = load_testfile(file_name)
        file_contents = [file_contents[0]]
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PySafetyBear',
                                'bottle<0.12.10 is vulnerable '
                                'to CVE-2016-9964 and your project '
                                'is using 0.10.0.',
                                file=get_testfile_path(file_name),
                                line=1,
                                column=9,
                                end_line=1,
                                end_column=15,
                                severity=RESULT_SEVERITY.NORMAL,
                                additional_info='redirect() in bottle.py '
                                'in bottle 0.12.10 doesn\'t filter '
                                'a "\\r\\n" sequence, which leads '
                                'to a CRLF attack, as demonstrated '
                                'by a redirect("233\\r\\nSet-Cookie: '
                                'name=salt") call.',
                                )],
            filename=get_testfile_path(file_name))

    def test_without_cve_vulnerability(self):
        file_name = 'requirement.txt'
        file_contents = load_testfile(file_name)
        file_contents = [file_contents[1]]
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('PySafetyBear',
                                'locustio<0.7 is vulnerable and '
                                'your project is using 0.5.1.',
                                file=get_testfile_path(file_name),
                                line=1,
                                column=11,
                                end_line=1,
                                end_column=16,
                                severity=RESULT_SEVERITY.NORMAL,
                                additional_info='locustio before '
                                '0.7 uses pickle.',
                                )],
            filename=get_testfile_path(file_name))

    def test_with_no_requirements(self):
        self.check_validity(self.uut, [])

    def test_with_no_pinned_requirements(self):
        self.check_validity(self.uut, ['foo'])
