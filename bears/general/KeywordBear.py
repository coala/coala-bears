import re

from coalib.bearlib import deprecate_settings
from coalib.bears.LocalBear import LocalBear
from coalib.results.Diff import Diff
from coalib.results.Result import RESULT_SEVERITY, Result

from bears.general.AnnotationBear import AnnotationBear
from coalib.results.SourceRange import SourceRange


def _get_comments(dependency_results):
    if not dependency_results:
        return {}

    annotation_bear_results = dependency_results.get('AnnotationBear')
    if (not annotation_bear_results or
            not isinstance(annotation_bear_results, list)):
        return {}

    comments = []
    for result in annotation_bear_results:
        if not isinstance(result.contents, dict):
            continue
        comments += list(result.contents.get('comments', []))
    return set(comments)


def generate_diff(dependency_results, file, filename,
                  line, line_number, pos):
    comments = _get_comments(dependency_results)
    diffs = None
    todo_source_range = SourceRange.from_values(filename, line_number + 1,
                                                pos + 1)
    for comment_sourcerange in comments:

        if todo_source_range not in comment_sourcerange:
            continue

        diff = Diff(file)
        comment_start = comment_sourcerange.start.column
        line_before_todo_comment = line[:comment_start - 1].strip()
        # remove just part of the line
        if (line_before_todo_comment and
                line_number + 1 == comment_sourcerange.start.line):
            diff.change_line(
                line_number + 1,
                line,
                line.replace(
                    line[comment_start - 1:], '').rstrip() + '\n')
        else:
            diff.delete_line(line_number + 1)

        diffs = {filename: diff}
    return diffs


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

        for line_number, line in enumerate(file):
            for keyword in keywords_regex.finditer(line):
                diffs = generate_diff(
                    dependency_results,
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
                    line=line_number + 1,
                    column=keyword.start() + 1,
                    end_line=line_number + 1,
                    end_column=keyword.end() + 1,
                    severity=RESULT_SEVERITY.INFO,
                    diffs=diffs)
