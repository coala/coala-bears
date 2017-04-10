from clang.cindex import Index, LibclangError

from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange
from coalib.settings.Setting import typed_list


def clang_available(cls):
    """
    Checks if Clang is available and ready to use.

    :return: True if Clang is available, a description of the error else.
    """
    try:
        Index.create()
        return True
    except LibclangError as error:  # pragma: no cover
        return str(error)


class ClangBear(LocalBear):
    LANGUAGES = {'C', 'C++', 'Objective-C', 'Objective-C++', 'OpenMP',
                 'OpenCL', 'CUDA'}
    # Depends on libclang-py3, which is a dependency of coala
    REQUIREMENTS = set()
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Variable Misuse', 'Syntax'}

    check_prerequisites = classmethod(clang_available)

    def run(self, filename, file, clang_cli_options: typed_list(str)=None):
        """
        Check code for syntactical or semantical problems using Clang.

        This bear supports automatic fixes.

        :param clang_cli_options: Any options that will be passed through to
                                  Clang.
        """
        index = Index.create()
        diagnostics = index.parse(
            filename,
            args=clang_cli_options,
            unsaved_files=[(filename, ''.join(file))]).diagnostics
        for diag in diagnostics:
            severity = {0: RESULT_SEVERITY.INFO,
                        1: RESULT_SEVERITY.INFO,
                        2: RESULT_SEVERITY.NORMAL,
                        3: RESULT_SEVERITY.MAJOR,
                        4: RESULT_SEVERITY.MAJOR}.get(diag.severity)
            affected_code = tuple(SourceRange.from_clang_range(range)
                                  for range in diag.ranges)

            diffs = None
            fixits = list(diag.fixits)
            if len(fixits) > 0:
                # FIXME: coala doesn't support choice of diffs, for now
                # append first one only, often there's only one anyway
                diffs = {filename: Diff.from_clang_fixit(fixits[0], file)}

                # No affected code yet? Let's derive it from the fix!
                if len(affected_code) == 0:
                    affected_code = diffs[filename].affected_code(filename)

            # Still no affected code? Position is the best we can get...
            if len(affected_code) == 0 and diag.location.file is not None:
                affected_code = (SourceRange.from_values(
                    diag.location.file.name,
                    diag.location.line,
                    diag.location.column),)

            yield Result(
                self,
                diag.spelling,
                severity=severity,
                affected_code=affected_code,
                diffs=diffs)
