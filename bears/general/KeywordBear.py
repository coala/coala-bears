import re

from coalib.bearlib import deprecate_settings
from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import RESULT_SEVERITY, Result
from coalib.results.SourceRange import SourceRange

from bears.general.AnnotationBear import AnnotationBear


def _get_comments(dependency_results):
    if not dependency_results:
        return

    annotation_bear_results = dependency_results.get('AnnotationBear')
    if (not annotation_bear_results or
            not isinstance(annotation_bear_results, list)):
        return

    for result in annotation_bear_results:
        yield from result.contents.get('comments', [])


def generate_diff(comments, file, filename,
                  line, line_number, pos):
    todo_source_range = SourceRange.from_values(filename, line_number,
                                                pos + 1)
    affected_comment_sourcerange = [
        c for c in comments if todo_source_range in c]

    affected_len = len(affected_comment_sourcerange)

    if affected_len == 0:
        return {}
    assert affected_len == 1, "More than 1 affected comment source ranges"

    comment_sourcerange = affected_comment_sourcerange[0]

    comment_start = comment_sourcerange.start.column
    comment_end = comment_sourcerange.end.column
    in_multi_line_comment = (
        comment_sourcerange.start.line != comment_sourcerange.end.line
    )

    line_before_todo_comment = line[:comment_start - 1].rstrip()
    line_behind_todo_comment = line[comment_end:].rstrip()

    line_replacement = line_before_todo_comment + line_behind_todo_comment

    diff = Diff(file)
    if line_replacement and not in_multi_line_comment:
        diff.change_line(
            line_number,
            line,
            line_replacement + '\n')
    elif line_replacement and in_multi_line_comment:
        text_replacement = line[pos:]
        diff.change_line(
            line_number,
            line,
            line.replace(text_replacement, '').rstrip() + '\n')
    else:
        diff.delete_line(line_number)

    return {filename: diff}


class KeywordBear(LocalBear):
    LANGUAGES = {"All"}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Documentation'}
    BEAR_DEPS = {AnnotationBear}

    @deprecate_settings(keywords='ci_keywords')
    def run(self,
            filename,
            file,
            keywords: list,
            dependency_results: dict=None):
        '''
        Checks the code files for given keywords.

        :param keywords:
            A list of keywords to search for (case insensitive).
            Usual examples are TODO and FIXME.
        '''
        keywords_regex = re.compile(
            '(' + '|'.join(re.escape(key) for key in keywords) + ')',
            re.IGNORECASE)

        comments = _get_comments(dependency_results)

        for line_number, line in enumerate(file, start=1):
            for keyword in keywords_regex.finditer(line):
                diffs = generate_diff(
                    comments,
                    file,
                    filename,
                    line,
                    line_number,
                    keyword.start())
                yield Result.from_values(
                    origin=self,
                    message="The line contains the keyword '{}'."
                            .format(keyword.group()),
                    file=filename,
                    line=line_number,
                    column=keyword.start() + 1,
                    end_line=line_number,
                    end_column=keyword.end() + 1,
                    severity=RESULT_SEVERITY.INFO,
                    diffs=diffs)
