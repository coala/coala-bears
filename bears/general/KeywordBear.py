import re
import logging

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
        if isinstance(result.contents, str):
            logging.error(result.contents)
        else:
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
    assert affected_len == 1, 'More than 1 affected comment source ranges'

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
    LANGUAGES = {'All'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Documentation'}
    BEAR_DEPS = {AnnotationBear}

    @deprecate_settings(keywords='ci_keywords')
    def run(self,
            filename,
            file,
            keywords: list=['todo', 'fixme'],
            regex_keyword: str='',
            dependency_results: dict=None):
        '''
        Checks the code files for given keywords.

        :param keywords:
            A list of keywords to search for (case insensitive).
            Default are TODO and FIXME.
        :param regex_keyword:
            A regular expression to search for matching keywords in a file.
        '''
        comments = list(_get_comments(dependency_results))

        if keywords:
            simple_keywords_regex = re.compile(
                '(' + '|'.join(re.escape(key) for key in keywords) + ')',
                re.IGNORECASE)

            message = "The line contains the keyword '{}'."
            yield from self.check_keywords(filename, file, comments,
                                           simple_keywords_regex, message)

        if regex_keyword is not '':
            regex = re.compile(regex_keyword)
            message = ("The line contains the keyword '{}' which "
                       'resulted in a match with given regex.')
            yield from self.check_keywords(filename, file, comments, regex,
                                           message)

    def check_keywords(self,
                       filename,
                       file,
                       comments,
                       regex,
                       message):
        '''
        Checks for the presence of keywords according to regex in a given file.

        :param regex:
           A regular expression which is used to search matching
           keywords in a file.
        :param message:
           A message to be displayed to the user when a keyword in a given file
           results in a match. It may have an unnamed placeholder for the
           keyword.
        '''

        for line_number, line in enumerate(file, start=1):
            for keyword in regex.finditer(line):
                diffs = generate_diff(
                    comments,
                    file,
                    filename,
                    line,
                    line_number,
                    keyword.start())
                yield Result.from_values(
                    origin=self,
                    message=message.format(keyword.group()),
                    file=filename,
                    line=line_number,
                    column=keyword.start() + 1,
                    end_line=line_number,
                    end_column=keyword.end() + 1,
                    severity=RESULT_SEVERITY.INFO,
                    diffs=diffs)
