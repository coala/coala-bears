import logging
import radon.complexity
import radon.visitors

from coalib.bears.LocalBear import LocalBear
from dependency_management.requirements.PythonImportRequirement import (
                PythonImportRequirement)
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange
from coalib.settings.Setting import typed_list


class RadonBear(LocalBear):
    LANGUAGES = {'Python', 'Python 2', 'Python 3'}
    REQUIREMENTS = {PythonImportRequirement('radon',
                                            '==1.4.0',
                                            ['radon.complexity',
                                             'radon.visitors'])}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Complexity'}

    def run(self, filename, file,
            cyclomatic_complexity: int = None,
            radon_ranks_info: typed_list(str) = (),
            radon_ranks_normal: typed_list(str) = ('C', 'D'),
            radon_ranks_major: typed_list(str) = ('E', 'F'),
            ):
        """
        Uses radon to compute complexity of a given file.

        :param cyclomatic_complexity: Maximum cyclomatic complexity
                                      that is considered to be normal.
        :param radon_ranks_info:      The ranks (given by radon) to
                                      treat as severity INFO.
        :param radon_ranks_normal:    The ranks (given by radon) to
                                      treat as severity NORMAL.
        :param radon_ranks_major:     The ranks (given by radon) to
                                      treat as severity MAJOR.
        """
        severity_map = {
            RESULT_SEVERITY.INFO: radon_ranks_info,
            RESULT_SEVERITY.NORMAL: radon_ranks_normal,
            RESULT_SEVERITY.MAJOR: radon_ranks_major
        }

        if cyclomatic_complexity is None:
            logging.warning('The settings `radon_ranks_info`, '
                            '`radon_ranks_normal` and `radon_ranks_major`'
                            ' are deprecated. Please use '
                            '`cyclomatic_complexity` instead.')

        for visitor in radon.complexity.cc_visit(''.join(file)):
            rank = radon.complexity.cc_rank(visitor.complexity)
            severity = None
            for result_severity, rank_list in severity_map.items():
                if rank in rank_list:
                    severity = result_severity

            if (cyclomatic_complexity is None and
                    severity is None):
                continue
            elif (cyclomatic_complexity and
                    visitor.complexity <= cyclomatic_complexity):
                severity = RESULT_SEVERITY.INFO
            else:
                severity = RESULT_SEVERITY.MAJOR

            col = visitor.col_offset if visitor.col_offset else None
            visitor_range = SourceRange.from_values(
                filename, visitor.lineno, col, visitor.endline)
            message = '{} has a cyclomatic complexity of {}'.format(
                visitor.name, visitor.complexity)

            yield Result(self, message, severity=severity,
                         affected_code=(visitor_range,))
