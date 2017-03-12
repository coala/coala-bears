from queue import Queue

from bears.general.LineCountBear import LineCountBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.results.Result import RESULT_SEVERITY, Result
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class LineCountBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.uut = LineCountBear(self.section, Queue())

    def test_run(self):
        self.section.append(Setting('max_lines_per_file', 1))
        self.check_results(
            self.uut, ['line 1', 'line 2', 'line 3'],
            [Result.from_values('LineCountBear',
                                'This file had 3 lines, which is 2 lines more '
                                'than the maximum limit specified.',
                                severity=RESULT_SEVERITY.NORMAL,
                                file='default')],
            filename='default')
        self.check_validity(self.uut, ['1 line'])
        self.check_validity(self.uut, [])  # Empty file

    def test_exclude_blank_lines(self):
        self.section.append(Setting('exclude_blank_lines', True))
        self.section.append(Setting('max_lines_per_file', 2))
        self.check_results(
            self.uut, ['line 1', ' ', 'line 2',
                       'line 3', '\n', '\t', ' line 4',
                       'line 5 ', ' line 6 ', '\t\tline 7',
                       '', '\t \n ', ' \t\n '],
            [Result.from_values('LineCountBear',
                                'This file had 7 lines, which is 5 lines more '
                                'than the maximum limit specified.',
                                severity=RESULT_SEVERITY.NORMAL,
                                file='default')],
            filename='default')

    def test_min_lines_per_file(self):
        self.section.append(Setting('max_lines_per_file', 10))
        self.section.append(Setting('min_lines_per_file', 5))
        self.check_results(
            self.uut, ['line 1', 'line 2', 'line 3', 'line 4'],
            [Result.from_values('LineCountBear',
                                'This file had 4 lines, which is 1 lines '
                                'fewer than the minimum required.',
                                severity=RESULT_SEVERITY.NORMAL,
                                file='default')],
            filename='default')

    def test_valid_settings(self):
        self.section.append(Setting('max_lines_per_file', 5))
        self.section.append(Setting('min_lines_per_file', 5))
        self.section.append(Setting('exclude_blank_lines', True))
        self.check_results(
            self.uut, ['line 1', 'line 2', '\tline 3', ' line 4 ', ' line 5',
                       '\n', ' ', '\t', '\t\n', '\t \n'],
            [],
            filename='default')
