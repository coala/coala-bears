from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.Diff import Diff
from coalib.results.SourceRange import SourceRange


class GitConflictMarkerBear(LocalBear):
    def run(self, filename, file):
        marker_free_code = []

        merge_conflict_starts = [line_number for line_number, line in
                                 enumerate(file) if
                                 line.startswith('<<<<<<< ')]

        merge_conflict_split = [line_number for line_number, line in
                                enumerate(file) if
                                line.startswith('=========')]

        merge_conflict_ends = [line_number for line_number, line in
                               enumerate(file) if
                               line.startswith('>>>>>>> ')]

        for line_number, line in enumerate(file):
            if (line_number not in merge_conflict_starts and
                line_number not in merge_conflict_split and
                    line_number not in merge_conflict_ends):
                marker_free_code.append(line)

        diffs = Diff.from_string_arrays(file, marker_free_code).split_diff()

        for diff in diffs:
            yield Result(self,
                         'Possible merge conflict marker found on these lines',
                         affected_code=(diff.range(filename),), 
                         diffs={filename: diff})
