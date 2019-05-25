from clang.cindex import Index, LibclangError

from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange
from coalib.settings.Setting import typed_list

from dependency_management.requirements.PipRequirement import PipRequirement

from pkg_resources import get_distribution


def clang_available(cls):
    """
    Checks if Clang is available and ready to use.

    :return: True if Clang is available, a description of the error else.
    """
    if get_distribution('libclang-py3').version != '3.4.0':
        return ClangBear.name + ' requires clang 3.4.0'

    try:
        Index.create()
        return True
    except LibclangError as error:  # pragma: no cover
        return str(error)


def diff_from_clang_fixit(fixit, file):
    """
    Creates a ``Diff`` object from a given clang fixit and the file contents.

    :param fixit: A ``cindex.Fixit`` object.
    :param file:  A list of lines in the file to apply the fixit to.
    :return:      The corresponding ``Diff`` object.
    """
    assert isinstance(file, (list, tuple))

    oldvalue = '\n'.join(file[fixit.range.start.line-1:
                              fixit.range.end.line])
    endindex = fixit.range.end.column - len(file[fixit.range.end.line-1])-1

    newvalue = (oldvalue[:fixit.range.start.column-1] +
                fixit.value +
                oldvalue[endindex:])
    new_file = (file[:fixit.range.start.line-1] +
                type(file)(newvalue.splitlines(True)) +
                file[fixit.range.end.line:])

    return Diff.from_string_arrays(file, new_file)


def sourcerange_from_clang_range(clang_range):
    """
    Creates a ``SourceRange`` from a clang ``SourceRange`` object.

    :param clang_range: A ``cindex.SourceRange`` object.
    """
    return SourceRange.from_values(clang_range.start.file.name,
                                   clang_range.start.line,
                                   clang_range.start.column,
                                   clang_range.end.line,
                                   clang_range.end.column)


class ClangBear(LocalBear):
    LANGUAGES = {'C', 'CPP', 'Objective-C', 'Objective-CPP', 'OpenMP',
                 'OpenCL', 'CUDA'}
    # Depends on libclang-py3, which is a dependency of coala
    REQUIREMENTS = {PipRequirement('libclang-py3', '3.4.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Variable Misuse', 'Syntax'}

    check_prerequisites = classmethod(clang_available)

    def run(self, filename, file,
            clang_cli_options: typed_list(str) = None,
            ):
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
            affected_code = tuple(sourcerange_from_clang_range(clang_range)
                                  for clang_range in diag.ranges)

            diffs = None
            fixits = list(diag.fixits)
            if len(fixits) > 0:
                # FIXME: coala doesn't support choice of diffs, for now
                # append first one only, often there's only one anyway
                diffs = {filename: diff_from_clang_fixit(fixits[0], file)}

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
