import attr

from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition
from coalib.bears.LocalBear import LocalBear
from coalib.results.HiddenResult import HiddenResult
from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.results.SourceRange import SourceRange
from coalib.results.AbsolutePosition import AbsolutePosition
from coala_utils.string_processing.Core import unescaped_search_for


class AnnotationBear(LocalBear):
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    def run(self, filename, file, language: str, coalang_dir: str = None):
        """
        Finds out all the positions of strings and comments in a file.
        The Bear searches for valid comments and strings and yields their
        ranges as SourceRange objects in HiddenResults.

        :param language:
            The programming language of the source code.
        :param coalang_dir:
            External directory for coalang file.
        :return:
            One HiddenResult containing a dictionary with keys being
            'singleline strings', 'multiline strings', 'singleline comments'
            and 'multiline comments' and values being a dictionary with
            keys ```'start_delimiter_range', 'end_delimiter_range'
            'content_range', 'full_range'```.
            The ranges do include string quotes or the comment
            starting separator but not anything before (e.g. when using
            ``u"string"``, the ``u`` will not be in the source range).
        """
        try:
            lang_dict = LanguageDefinition(language, coalang_dir=coalang_dir)
        except FileNotFoundError:
            content = ('coalang specification for ' + language +
                       ' not found.')
            yield HiddenResult(self, content)
            return

        string_delimiters = dict(lang_dict['string_delimiters'])
        multiline_string_delimiters = dict(
            lang_dict['multiline_string_delimiters'])
        multiline_comment_delimiters = dict(
            lang_dict['multiline_comment_delimiters'])
        comment_delimiter = dict(lang_dict['comment_delimiter'])
        ranges = []
        try:
            ranges = self.find_annotation_ranges(
                file,
                filename,
                string_delimiters,
                multiline_string_delimiters,
                comment_delimiter,
                multiline_comment_delimiters)

        except NoCloseError as e:
            yield Result(self, str(e), severity=RESULT_SEVERITY.MAJOR,
                         affected_code=(e.code,))

        content = AnnotationContent(ranges)
        yield HiddenResult(self, content)

    def find_annotation_ranges(self,
                               file,
                               filename,
                               string_delimiters,
                               multiline_string_delimiters,
                               comment_delimiter,
                               multiline_comment_delimiters):
        """
        Finds ranges of all annotations.

        :param file:
            A tuple of strings, with each string being a line in the file.
        :param filename:
            The name of the file.
        :param string_delimiters:
            A dictionary containing the various ways to  define single-line
            strings in a language.
        :param multiline_string_delimiters:
            A dictionary containing the various ways to define multi-line
            strings in a language.
        :param comment_delimiter:
            A dictionary containing the various ways to define single-line
            comments in a language.
        :param multiline_comment_delimiters:
            A dictionary containing the various ways to define multi-line
            comments in a language.
        :return:
            Four tuples containing dictionary for singleline strings,
            multiline strings, singleline comments and multiline comments
            respectively.
        """
        text = ''.join(file)
        annotations_range = []
        position = 0

        while position <= len(text):

            def get_new_position():
                end_position, start_delim, end_delim = (
                    self.get_range_end_position(
                        file,
                        filename,
                        text,
                        multiline_string_delimiters,
                        position,
                        self.get_multiline))
                if end_position:
                    seperate_ranges = get_seperate_ranges(file,
                                                          filename,
                                                          start_delim,
                                                          end_delim,
                                                          position,
                                                          end_position)
                    annotations_range.append(AnnotationRange(
                        'multiline_string', seperate_ranges))
                    return end_position + 1

                end_position, start_delim, end_delim = (
                    self.get_range_end_position(
                        file,
                        filename,
                        text,
                        string_delimiters,
                        position,
                        self.get_singleline_strings))
                if end_position:
                    seperate_ranges = get_seperate_ranges(file,
                                                          filename,
                                                          start_delim,
                                                          end_delim,
                                                          position,
                                                          end_position)
                    annotations_range.append(AnnotationRange(
                        'singleline_string', seperate_ranges))
                    return end_position + 1

                end_position, start_delim, end_delim = (
                    self.get_range_end_position(
                        file,
                        filename,
                        text,
                        multiline_comment_delimiters,
                        position,
                        self.get_multiline))
                if end_position:
                    seperate_ranges = get_seperate_ranges(file,
                                                          filename,
                                                          start_delim,
                                                          end_delim,
                                                          position,
                                                          end_position)
                    annotations_range.append(AnnotationRange(
                        'multiline_comment', seperate_ranges))
                    return end_position + 1

                end_position, start_delim, end_delim = (
                    self.get_range_end_position(
                        file,
                        filename,
                        text,
                        comment_delimiter,
                        position,
                        self.get_singleline_comment,
                        single_comment=True))
                if end_position:
                    seperate_ranges = get_seperate_ranges(file,
                                                          filename,
                                                          start_delim,
                                                          end_delim,
                                                          position,
                                                          end_position)
                    annotations_range.append(AnnotationRange(
                        'singleline_comment', seperate_ranges))
                    return end_position + 1

                return position + 1

            position = get_new_position()

        return annotations_range

    @staticmethod
    def get_range_end_position(file,
                               filename,
                               text,
                               annotations,
                               position,
                               func,
                               single_comment=False):
        selected_annotation = end_position = selected_end_annotation = None
        for annotation in annotations.keys():
            if text[position:].startswith(annotation):
                selected_annotation = annotation
                if not single_comment:
                    selected_end_annotation = annotations[selected_annotation]
                    end_position = func(file,
                                        filename,
                                        text,
                                        annotation,
                                        annotations[annotation],
                                        position)
                else:
                    selected_end_annotation = '\n'
                    end_position = func(file,
                                        filename,
                                        text,
                                        annotation,
                                        position)

        return end_position, selected_annotation, selected_end_annotation

    @staticmethod
    def get_multiline(file,
                      filename,
                      text,
                      annotation_start,
                      annotation_end,
                      position):
        """
        Gets sourcerange and end position of an annotation that can span
        multiple lines.

        :param file:
            A tuple of strings, with each string being a line in the file.
        :param filename:
            The name of the file.
        :param annotation_start:
            The string specifying the start of the annotation.
        :param annotation_end:
            The string specifying the end of the annotation.
        :param position:
            An integer identifying the position where the annotation started.
        :return:
            The end_position of the annotation as an integer.
        """
        end_end = get_end_position(annotation_end,
                                   text,
                                   position + len(annotation_start) - 1)
        if end_end == -1:
            _range = SourceRange.from_absolute_position(
                filename,
                AbsolutePosition(file, position))
            raise NoCloseError(annotation_start, _range)

        return end_end

    @staticmethod
    def get_singleline_strings(file,
                               filename,
                               text,
                               string_start,
                               string_end,
                               position):
        """
        Gets sourcerange of a single-line string and its end position.

        :param file:
            A tuple of strings, with each string being a line in the file.
        :param filename:
            The name of the file.
        :param string_start:
            The string which specifies how a string starts.
        :param string_end:
            The string which specifies how a string ends.
        :position:
            An integer identifying the position where the string started.
        :return:
            The end_position of the string as an integer.
        """
        end_position = get_end_position(string_end,
                                        text,
                                        position + len(string_start) - 1)
        newline = get_end_position('\n', text, position)
        if newline == -1:
            newline = len(text)
        if end_position == -1:
            _range = SourceRange.from_absolute_position(
                filename,
                AbsolutePosition(file, position))
            raise NoCloseError(string_start, _range)
        if newline > end_position:
            return end_position

    @staticmethod
    def get_singleline_comment(file, filename, text, comment, position):
        """
        Gets Sourcerange of a single-line comment where the start is the
        start of comment and the end is the end of line.

        :param file:
            A tuple of strings, with each string being a line in the file.
        :param filename:
            The name of the file.
        :param comment:
            The string which specifies the comment.
        :position:
            An integer identifying the position where the string started.
        :return:
            The end_position of the comment as an integer.
        """
        end_position = get_end_position('\n',
                                        text,
                                        position + len(comment) - 1)
        if end_position == -1:
            end_position = len(text) - 1
        return end_position


def get_end_position(end_marker, text, position):
    try:
        end_match = next(unescaped_search_for(end_marker, text[position + 1:]))
        end_position = position + end_match.span()[1]
    except StopIteration:
        end_position = -1

    return end_position


def get_seperate_ranges(file,
                        filename,
                        start_delim,
                        end_delim,
                        start_position,
                        end_position):
    ranges = []
    ranges.append(SourceRange.from_absolute_position(
        filename,
        AbsolutePosition(file, start_position),
        AbsolutePosition(file, start_position + len(start_delim) - 1)))

    ranges.append(SourceRange.from_absolute_position(
        filename,
        AbsolutePosition(file, end_position - len(end_delim) + 1),
        AbsolutePosition(file, end_position)))

    if start_position + 1 == end_position:  # empty string so no content
        ranges.append([])
    else:
        ranges.append(SourceRange.from_absolute_position(
            filename,
            AbsolutePosition(file, start_position + len(start_delim)),
            AbsolutePosition(file, end_position - len(end_delim))))

    ranges.append(SourceRange.from_absolute_position(
        filename,
        AbsolutePosition(file, start_position),
        AbsolutePosition(file, end_position)))

    return ranges


class NoCloseError(Exception):

    def __init__(self, annotation, code):
        Exception.__init__(self, annotation + ' has no closure')
        self.code = code


@attr.s
class AnnotationRange:

    AnnotationType = attr.ib(convert=str)
    range = attr.ib()
    start_delimiter_range = attr.ib(init=False)
    end_delimiter_range = attr.ib(init=False)
    content_range = attr.ib(init=False)
    full_range = attr.ib(init=False)

    def __attrs_post_init__(self):
        if len(self.range) == 4:
            self.start_delimiter_range = self.range[0]
            self.end_delimiter_range = self.range[1]
            self.content_range = self.range[2]
            self.full_range = self.range[3]
        else:
            self.start_delimiter_range = []
            self.end_delimiter_range = []
            self.content_range = []
            self.full_range = []


@attr.s
class AnnotationContent:

    singleline_strings = attr.ib(init=False)
    multiline_strings = attr.ib(init=False)
    singleline_comments = attr.ib(init=False)
    multiline_comments = attr.ib(init=False)
    ranges = attr.ib()

    def __attrs_post_init__(self):
        single_strings = []
        multi_strings = []
        single_comments = []
        multi_comments = []
        for range in self.ranges:
            if range.AnnotationType == 'singleline_string':
                single_strings.append(range)
            elif range.AnnotationType == 'multiline_string':
                multi_strings.append(range)
            elif range.AnnotationType == 'multiline_comment':
                multi_comments.append(range)
            elif range.AnnotationType == 'singleline_comment':
                single_comments.append(range)
        self.singleline_strings = single_strings
        self.multiline_strings = multi_strings
        self.singleline_comments = single_comments
        self.multiline_comments = multi_comments
