from queue import Queue
import logging

from bears.general.LineCountBear import LineCountBear
from coalib.testing.LocalBearTestHelper import LocalBearTestHelper
from coalib.testing.LocalBearTestHelper import execute_bear
from coalib.results.Result import RESULT_SEVERITY, Result
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class LineCountBearTest(LocalBearTestHelper):

    def setUp(self):
        self.section = Section('name')
        self.uut = LineCountBear(self.section, Queue())

    def test_run(self):
        self.section.append(Setting('min_lines_per_file', 0))
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
        self.section.append(Setting('min_lines_per_file', 0))
        self.section.append(Setting('max_lines_per_file', 2))
        self.section.append(Setting('exclude_blank_lines', True))
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

    def test_range_allowed_for_lines_per_file(self):
        self.section.append(Setting('min_lines_per_file', 5))
        self.section.append(Setting('max_lines_per_file', 10))
        self.section.append(Setting('exclude_blank_lines', True))
        self.check_results(
            self.uut, ['line 1', '', 'line 2', '', 'line 3', 'line 4'],
            [Result.from_values('LineCountBear',
                                'This file has 4 lines, while 5 lines '
                                'are required.',
                                severity=RESULT_SEVERITY.NORMAL,
                                file='default')],
            filename='default')

    def test_one_element_range(self):
        self.section.append(Setting('min_lines_per_file', 5))
        self.section.append(Setting('max_lines_per_file', 5))
        self.section.append(Setting('exclude_blank_lines', True))
        self.check_results(
            self.uut, ['line 1', 'line 2', '\tline 3', ' line 4 ', ' line 5',
                       '\n', ' ', '\t', '\t\n', '\t \n'],
            [],
            filename='default')

    def test_default_min_lines_per_file(self):
        self.section.append(Setting('max_lines_per_file', 2))
        self.section.append(Setting('exclude_blank_lines', True))
        self.check_results(
            self.uut, [''],
            [Result.from_values('LineCountBear',
                                'This file has 0 lines, while 1 lines '
                                'are required.',
                                severity=RESULT_SEVERITY.NORMAL,
                                file='default')],
            filename='default')

    def test_min_limit_exceeds_max_limit(self):
        EXCEPTION_MESSAGE = ('ERROR:root:Allowed maximum lines per file (1) '
                             'is smaller than minimum lines per file (2)')
        self.section.append(Setting('min_lines_per_file', 2))
        self.section.append(Setting('max_lines_per_file', 1))
        self.section.append(Setting('exclude_blank_lines', True))
        logger = logging.getLogger()

        with self.assertLogs(logger, 'ERROR') as log:
            with execute_bear(self.uut, filename='F', file='') as result:
                self.assertEqual(len(log.output), 1)
                self.assertEqual(log.output[0], EXCEPTION_MESSAGE)
