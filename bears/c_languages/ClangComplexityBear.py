from clang.cindex import Index, CursorKind

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.bearlib import deprecate_settings
from bears.c_languages.ClangBear import (
    clang_available, ClangBear, sourcerange_from_clang_range,
)


class ClangComplexityBear(LocalBear):
    """
    Calculates cyclomatic complexity of each function and displays it to the
    user.
    """

    LANGUAGES = ClangBear.LANGUAGES
    REQUIREMENTS = ClangBear.REQUIREMENTS
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Complexity'}

    check_prerequisites = classmethod(clang_available)
    _decisive_cursor_kinds = {
        CursorKind.IF_STMT, CursorKind.WHILE_STMT, CursorKind.FOR_STMT,
        CursorKind.DEFAULT_STMT, CursorKind.CASE_STMT}

    def function_key_points(self, cursor, top_function_level=False):
        """
        Calculates number of function's decision points and exit points.

        :param top_function_level: Whether cursor is in the top level of
                                   the function.
        """
        decisions, exits = 0, 0

        for child in cursor.get_children():
            if child.kind in self._decisive_cursor_kinds:
                decisions += 1
            elif child.kind == CursorKind.RETURN_STMT:
                exits += 1
                if top_function_level:
                    # There is no point to move forward, so just return.
                    return decisions, exits
            child_decisions, child_exits = self.function_key_points(child)
            decisions += child_decisions
            exits += child_exits

        if top_function_level:
            # Implicit return statement.
            exits += 1

        return decisions, exits

    def complexities(self, cursor, filename):
        """
        Calculates cyclomatic complexities of functions.
        """

        file = cursor.location.file

        if file is not None and file.name != filename:
            # There is nothing to do in another file.
            return

        if cursor.kind == CursorKind.FUNCTION_DECL:
            child = next((child for child in cursor.get_children()
                          if child.kind != CursorKind.PARM_DECL),
                         None)
            if child:
                decisions, exits = self.function_key_points(child, True)
                complexity = max(1, decisions - exits + 2)
                yield cursor, complexity
        else:
            for child in cursor.get_children():
                yield from self.complexities(child, filename)

    @deprecate_settings(cyclomatic_complexity='max_complexity')
    def run(self, filename, file,
            cyclomatic_complexity: int = 8,
            ):
        """
        Check for all functions if they are too complicated using the
        cyclomatic complexity metric.

        You can read more about this metric at
        <https://www.wikiwand.com/en/Cyclomatic_complexity>.

        :param cyclomatic_complexity:  Maximum cyclomatic complexity that is
                                considered to be normal. The value of 10 had
                                received substantial corroborating evidence.
                                But the general recommendation: "For each
                                module, either limit cyclomatic complexity to
                                [the agreed-upon limit] or provide a written
                                explanation of why the limit was exceeded."
        """

        root = Index.create().parse(filename).cursor
        for cursor, complexity in self.complexities(root, filename):
            if complexity > cyclomatic_complexity:
                affected_code = (sourcerange_from_clang_range(cursor.extent),)
                yield Result(
                    self,
                    "The function '{function}' should be simplified. Its "
                    'cyclomatic complexity is {complexity} which exceeds '
                    'maximal recommended value '
                    'of {rec_value}.'.format(
                        function=cursor.displayname,
                        complexity=complexity,
                        rec_value=cyclomatic_complexity),
                    affected_code=affected_code,
                    additional_info=(
                        'The cyclomatic complexity is a metric that measures '
                        'how complicated a function is by counting branches '
                        'and exits of each function.\n\n'
                        'Your function seems to be complicated and should be '
                        'refactored so that it can be understood by other '
                        'people easily.\n\nSee '
                        '<http://www.wikiwand.com/en/Cyclomatic_complexity>'
                        ' for more information.'))
