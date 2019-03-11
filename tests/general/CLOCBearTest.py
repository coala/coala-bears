import os
from queue import Queue

from coalib.settings.Section import Section
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result

from bears.general.CLOCBear import CLOCBear


def get_absolute_test_path(file):
    return os.path.join(os.path.dirname(__file__),
                        'cloc_test_files', file)


def load_testfile(name):
    with open(get_absolute_test_path(name)) as file:
        return file.readlines()


@generate_skip_decorator(CLOCBear)
class CLOCBearTest(LocalBearTestHelper):

    def setUp(self):
        self.uut = CLOCBear(Section('name'), Queue())
        self.test_files = ['example1.cpp', 'example2.py',
                           'example3.cpp', 'example4.txt']
        self.expected_results = {self.test_files[0]: {'LANGUAGE': 'C++',
                                                      'FILES': 1,
                                                      'CODE': 6,
                                                      'COMMENTS': 5,
                                                      'BLANK': 3},
                                 self.test_files[1]: {'LANGUAGE': 'Python',
                                                      'FILES': 1,
                                                      'CODE': 3,
                                                      'COMMENTS': 2,
                                                      'BLANK': 2},
                                 self.test_files[2]: {'LANGUAGE': 'C++',
                                                      'FILES': 1,
                                                      'CODE': 11,
                                                      'COMMENTS': 0,
                                                      'BLANK': 3},
                                 self.test_files[3]: 'File does not belong '
                                                     'to valid programming '
                                                     'language.'
                                 }

    def build_message(self, filename):
        result = self.expected_results[filename]

        lang = result['LANGUAGE']
        nfiles = result['FILES']
        code = result['CODE']
        comment = result['COMMENTS']
        blank = result['BLANK']
        total = code + comment + blank

        message = '\n'.join(['Language: {0}'.format(lang),
                             'Total files: {0}'.format(nfiles),
                             'Total lines: {0}'.format(total),
                             'Code lines: {0} ({1:.2f}%)'.format(
                               code, code * 100.0 / total),
                             'Comment lines: {0} ({1:.2f}%)'.format(
                               comment, comment * 100.0 / total),
                             'Blank lines: {0} ({1:.2f}%)'.format(
                               blank, blank * 100.0 / total)
                             ])
        return message

    def test_valid(self):
        for filename in self.test_files[:-1]:
            file_contents = load_testfile(filename)
            self.check_results(
                self.uut,
                file_contents,
                [Result.from_values('CLOCBear',
                                    self.build_message(filename),
                                    file=get_absolute_test_path(filename),
                                    severity=RESULT_SEVERITY.INFO)],
                filename=get_absolute_test_path(filename))

    def test_invalid(self):
        filename = self.test_files[3]
        file_contents = load_testfile(filename)
        self.check_results(
            self.uut,
            file_contents,
            [Result.from_values('CLOCBear',
                                str(self.expected_results[filename]),
                                file=get_absolute_test_path(filename),
                                severity=RESULT_SEVERITY.MAJOR)],
            filename=get_absolute_test_path(filename))
