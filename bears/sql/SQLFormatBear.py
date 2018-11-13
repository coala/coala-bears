import sqlparse

from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import Result
from dependency_management.requirements.PipRequirement import PipRequirement


class SQLFormatBear(LocalBear):
    LANGUAGES = {'SQL'}
    REQUIREMENTS = {PipRequirement('sqlparse', '0.2.4')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}

    def run(self,
            filename,
            file,
            keyword_case: str = 'upper',
            identifier_case: str = 'lower',
            strip_comments: bool = False,
            reindent: bool = True,
            indent_tabs: bool = False,
            indent_width: int = 4):
        """
        Linter for SQL language based on sqlparse.
        More info: https://github.com/andialbrecht/sqlparse

        :param keyword_case:
            Changes how keywords are formatted.
            Allowed values are `upper`, `lower` and `capitalize`.
        :param identifier_case:
            Changes how identifiers are formatted.
            Allowed values are `upper`, `lower`, and `capitalize`.
        :param strip_comments:
            If True comments are removed from the statements.
        :param reindent:
            If True the indentations of the statements are changed.
        :param indent_tabs:
            If True tabs instead of spaces are used for indentation.
        :param indent_width:
            The width of the indentation.
        """
        corrected = sqlparse.format(''.join(file),
                                    keyword_case=keyword_case,
                                    identifier_case=identifier_case,
                                    strip_comments=strip_comments,
                                    reindent=reindent,
                                    indent_tabs=indent_tabs,
                                    indent_width=indent_width,
                                    )

        corrected = corrected.splitlines(True)
        diffs = Diff.from_string_arrays(file, corrected).split_diff()

        for diff in diffs:
            yield Result(self,
                         'The code format can be improved.',
                         affected_code=(diff.range(filename),),
                         diffs={filename: diff})
