from coalib.parsing.StringProcessing.Core import (unescaped_search_in_between,
                                                  unescaped_search_for)
from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition
from coalib.bears.LocalBear import LocalBear
from coalib.results.HiddenResult import HiddenResult
from coalib.results.SourceRange import SourceRange
from coalib.results.AbsolutePosition import AbsolutePosition


class AnnotationBear(LocalBear):

    def run(self, filename, file, language: str, language_family: str):
        """
        Finds out all the positions of strings and comments in a file.
        The Bear searches for valid comments and strings and yields their
        ranges as SourceRange objects in HiddenResults.

        :param language:        Language to be whose annotations are to be
                                searched.
        :param language_family: Language family whose annotations are to be
                                searched.
        :return:                HiddenResults containing a dictionary with
                                keys as 'strings' or 'comments' and values as
                                a tuple of SourceRanges of strings and
                                a tuple of SourceRanges of comments
                                respectively.
        """
        lang_dict = LanguageDefinition(language, language_family)
        # Strings
        # TODO treat single-line and multiline strings differently
        strings = dict(lang_dict["string_delimiters"])
        strings.update(lang_dict["multiline_string_delimiters"])
        strings_found = self.find_with_start_end(filename, file, strings)
        # multiline Comments
        comments_found = self.find_with_start_end(
                filename, file, dict(lang_dict["multiline_comment_delimiters"]))
        # single-line Comments
        comments_found.update(self.find_singleline_comments(
                          filename, file, list(lang_dict["comment_delimiter"])))

        matches_found = strings_found | comments_found
        # Remove Nested
        unnested_annotations = set(filter(
                                       lambda arg: not starts_within_ranges(
                                           arg, matches_found),
                                       matches_found))
        # Yield different results for strings and comments
        strings_found = tuple(filter(lambda arg: arg in unnested_annotations,
                                     strings_found))
        comments_found = tuple(filter(lambda arg: arg in unnested_annotations,
                                      comments_found))
        yield HiddenResult(self, {'comments': comments_found,
                                  'strings': strings_found})

    @staticmethod
    def find_with_start_end(filename, file, annot):
        """
        Gives all positions of annotations which have a start and end.

        :param filename: Name of the file on which the bear is running.
        :param file:     Contents of the file in the form of tuple of lines.
        :param annot:    A dict containing start of annotation as key and end of
                         annotation as value.
        :return:         A set of SourceRanges giving the range of annotation.
        """
        text = ''.join(file)
        found_pos = set()
        for annot_type in annot:
            found_pos.update(unescaped_search_in_between(
                                           annot_type, annot[annot_type], text))
        if found_pos:
            found_pos = set(SourceRange.from_absolute_position(
                                filename,
                                AbsolutePosition(file, position.begin.range[0]),
                                AbsolutePosition(
                                    file, position.end.range[1] - 1))
                            for position in found_pos)
        return found_pos

    @staticmethod
    def find_singleline_comments(filename, file, comments):
        """
        Finds all single-line comments.

        :param filename: Name of the file on which the bear is running.
        :param file:     Contents of the file in the form of tuple of lines.
        :param comments: A list containing different types of
                         single-line comments.
        :return:         A set of SourceRange objects with start as the
                         beginning of the comment and end as
                         the termination of line.
        """
        text = ''.join(file)
        single_comments = set()
        for comment_type in comments:
            for found in unescaped_search_for(comment_type, text):
                start = found.start()
                end = text.find('\n', start)
                end = len(text) - 1 if end == -1 else end
                single_comments.add(SourceRange.from_absolute_position(
                                        filename,
                                        AbsolutePosition(file, start),
                                        AbsolutePosition(file, end)))
        return single_comments


def starts_within_ranges(inside_range, outside_ranges):
    """
    Finds if a particular range starts inside a collection of given ranges.

    :param outside_ranges: SourceRange identifying range to be searched.
    :param inside_range:   A tuple SourceRange objects identifying ranges
                           to be searched in.
    :return:               True if inside_range is found inside any of the
                           ranges given by outside_ranges, else
                           False is returned.
    """
    for outside_range in outside_ranges:
        if inside_range == outside_range:
            continue
        # Special case of python language.
        # Where doc strings (""") and strings (") have a similar start.
        elif inside_range.start == outside_range.start:
            if inside_range.end < outside_range.end:
                return True
        elif (inside_range.start > outside_range.start and
              inside_range.start <= outside_range.end):
            return True
    return False
