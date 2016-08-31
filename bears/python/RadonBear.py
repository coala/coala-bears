import radon.complexity
import radon.visitors

from coalib.bears.LocalBear import LocalBear
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange
from coalib.settings.Setting import typed_list


class RadonBear(LocalBear):
    LANGUAGES = {"Python", "Python 2", "Python 3"}
    REQUIREMENTS = {PipRequirement('radon', '1.*')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Complexity'}

    def run(self, filename, file,
            radon_ranks_info: typed_list(str)=(),
            radon_ranks_normal: typed_list(str)=('C', 'D'),
            radon_ranks_major: typed_list(str)=('E', 'F')):
        """
        Uses radon to compute complexity of a given file.

        :param radon_ranks_info:   The ranks (given by radon) to
                                   treat as severity INFO.
        :param radon_ranks_normal: The ranks (given by radon) to
                                   treat as severity NORMAL.
        :param radon_ranks_major:  The ranks (given by radon) to
                                   treat as severity MAJOR.
        """
        severity_map = {
            RESULT_SEVERITY.INFO: radon_ranks_info,
            RESULT_SEVERITY.NORMAL: radon_ranks_normal,
            RESULT_SEVERITY.MAJOR: radon_ranks_major
        }
        for visitor in radon.complexity.cc_visit("".join(file)):
            rank = radon.complexity.cc_rank(visitor.complexity)
            severity = None
            for result_severity, rank_list in severity_map.items():
                if rank in rank_list:
                    severity = result_severity
            if severity is None:
                continue

            col = visitor.col_offset if visitor.col_offset else None
            visitor_range = SourceRange.from_values(
                filename, visitor.lineno, col, visitor.endline)
            message = "{} has a cyclomatic complexity of {}".format(
                visitor.name, rank)

            yield Result(self, message, severity=severity,
                         affected_code=(visitor_range,))
