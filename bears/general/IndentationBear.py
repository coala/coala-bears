from coala_utils.string_processing.Core import unescaped_search_for
from coalib.bears.LocalBear import LocalBear
from coalib.bearlib import deprecate_settings
from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.results.SourceRange import SourceRange
from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.results.AbsolutePosition import AbsolutePosition
from coalib.results.Diff import Diff

from bears.general.AnnotationBear import AnnotationBear
from bears.general.RangeHelpers import (get_specified_block_range,
                                        get_valid_sequences)
from bears.general.CustomExceptions import (UnmatchedIndentError,
                                            ExpectedIndentError)


class IndentationBear(LocalBear):

    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}
    BEAR_DEPS = {AnnotationBear}  # pragma: no cover

    @deprecate_settings(indent_size='tab_width')
    def run(self,
            filename,
            file,
            dependency_results: dict,
            language: str,
            use_spaces: bool=True,
            indent_size: int=SpacingHelper.DEFAULT_TAB_WIDTH,
            indent_on_keywords: bool=False,
            coalang_dir: str=None):
        """
        It is a generic indent bear, which looks for a start and end
        indent specifier, example: ``{ : }`` where "{" is the start indent
        specifier and "}" is the end indent specifier. If the end-specifier
        is not given, this bear looks for unindents within the code to
        correctly figure out indentation.

        It also figures out hanging indents and absolute indentation of
        function params or list elements.

        It also supports indents based on keywords.
        for example:

            if(something)
            gets indented

        changes to:

            if(something)
                gets indented

        if the setting ``indent_on_keywords`` is true.

        WARNING: The IndentationBear is experimental right now, you can report
        any issues found to https://github.com/coala-analyzer/coala-bears

        :param filename:
            Name of the file that needs to be checked.
        :param file:
            File that needs to be checked in the form of a list of strings.
        :param dependency_results:
            Results given by the AnnotationBear.
        :param language:
            Language to be used for indentation.
        :param use_spaces:
            Insert spaces instead of tabs for indentation.
        :param indent_size:
            Number of spaces per indentation level.
        :param indent_on_keywords:
            If True it treats some keywords as indent specifiers and
            indents the statement that follows.
        :param coalang_dir:
            Full path of external directory containing the coalang
            file for language.
        """
        ranges = {}
        lang_settings_dict = LanguageDefinition(
            language, coalang_dir=coalang_dir)
        annotation_dict = dependency_results[AnnotationBear.name][0].contents
        # sometimes can't convert strings with ':' to dict correctly
        if ':' in list(lang_settings_dict['indent_types']):
            indent_types = dict(lang_settings_dict['indent_types'])
            indent_types[':'] = ''
        else:
            indent_types = dict(lang_settings_dict['indent_types'])

        indent_keywords = []
        if indent_on_keywords:
            try:
                indent_keywords = list(lang_settings_dict['indent_keywords'])
            except IndexError:  # pragma: no cover
                return [Result(self,
                               'indent_keywords specification not in coalang',
                               RESULT_SEVERITY.MAJOR)]

        encapsulators = (dict(lang_settings_dict['encapsulators']) if
                         'encapsulators' in lang_settings_dict else {})
        ranges['strings'] = annotation_dict['singleline strings'] + \
            annotation_dict['multiline strings']
        ranges['comments'] = annotation_dict['singleline comments'] + \
            annotation_dict['multiline comments']
        ranges['encapsulators'] = self._calculate_encapsulators_range(
            file,
            filename,
            encapsulators,
            ranges)
        comments = dict(lang_settings_dict['comment_delimiter'])
        comments.update(
            dict(lang_settings_dict['multiline_comment_delimiters']))

        indent_ranges = []
        try:
            for indent_specifier in indent_types:
                if indent_types[indent_specifier]:
                    indent_ranges += get_specified_block_range(
                        file,
                        filename,
                        indent_specifier,
                        indent_types[indent_specifier],
                        ranges)
                else:
                    indent_ranges += self.get_unspecified_block_range(
                        file,
                        filename,
                        indent_specifier,
                        ranges,
                        comments)
        # This happens only in case of unmatched indents or
        # ExpectedIndentError.
        except (UnmatchedIndentError, ExpectedIndentError) as e:
            yield Result(self, str(e), severity=RESULT_SEVERITY.MAJOR)
            return

        indent_ranges = sorted(indent_ranges, key=lambda x: (x.start.line,
                                                             x.start.column))
        ranges['indent_ranges'] = indent_ranges

        indent_levels = self.get_indent_levels(
            file,
            filename,
            indent_types,
            ranges,
            comments)
        ranges['indent_levels'] = indent_levels
        keyword_indent_levels = self._get_indent_keywords_range(
            file,
            filename,
            indent_keywords,
            ranges)

        absolute_indent_levels = self.get_absolute_indent_of_range(
            file,
            filename,
            ranges,
            encapsulators)

        insert = ' '*indent_size if use_spaces else '\t'

        no_indent_file = self._get_no_indent_file(file)
        new_file = self._get_basic_indent_file(no_indent_file,
                                               indent_levels,
                                               insert)
        if indent_on_keywords:
            new_file = self._get_keyword_indented_file(new_file,
                                                       keyword_indent_levels,
                                                       ranges,
                                                       insert)
        new_file = self._get_absolute_indent_file(new_file,
                                                  absolute_indent_levels,
                                                  indent_levels,
                                                  insert)

        if new_file != list(file):
            wholediff = Diff.from_string_arrays(file, new_file)
            for diff in wholediff.split_diff():
                yield Result(
                    self,
                    'The indentation could be changed to improve readability.',
                    severity=RESULT_SEVERITY.INFO,
                    affected_code=(diff.range(filename),),
                    diffs={filename: diff})

    def _get_indent_keywords_range(self,
                                   file,
                                   filename,
                                   indent_keywords,
                                   ranges):
        keyword_pos = {}
        for keyword in indent_keywords:
            keyword_pos[keyword] = (tuple(get_valid_sequences(file,
                                                              keyword,
                                                              ranges,
                                                              keyword=True)))
        keyword_range = []
        for keyword in keyword_pos:
            for position in keyword_pos[keyword]:
                start = position
                end = AbsolutePosition(file, position.position + len(keyword))
                end = self._find_last_range(start.line,
                                            end,
                                            ranges['encapsulators'])
                indent = True
                for _range in ranges['indent_ranges']:
                    if(_range.start.line == end.line and
                            _range.start.column > position.column):
                        indent = False
                        break
                if indent:
                    keyword_range.append(SourceRange.from_values(
                        filename,
                        start_line=start.line,
                        start_column=start.column,
                        end_line=end.line,
                        end_column=end.column))
        return keyword_range

    def _find_last_range(self, start_line, end, ranges):
        for _range in ranges:
            if (_range.start.line == start_line and
                    _range.end.line > end.line):
                end = _range.end
        return end

    def _get_keyword_indented_file(self,
                                   file,
                                   keyword_ranges,
                                   ranges,
                                   insert):
        for _range in keyword_ranges:
            prev_indent = get_indent_of_line(file,
                                             _range.start.line - 1,
                                             length=False)
            file[_range.end.line] = (prev_indent + insert +
                                     file[_range.end.line].lstrip())
            start_line = _range.end.line + 1
            end = _range.end
            end = self._find_last_range(start_line,
                                        end,
                                        ranges['indent_ranges'])
            for line in range(start_line, end.line):
                file[line] = (prev_indent + insert +
                              insert*ranges['indent_levels'][line] +
                              file[line].lstrip())

        return file

    def _calculate_encapsulators_range(self,
                                       file,
                                       filename,
                                       encapsulators,
                                       ranges):
        encaps_pos = sorted(tuple(_range
                                  for encapsulator in encapsulators
                                  for _range in get_specified_block_range(
                                      file,
                                      filename,
                                      encapsulator,
                                      encapsulators[encapsulator],
                                      ranges)))
        return encaps_pos

    def _get_no_indent_file(self, file):
        no_indent_file = [line.lstrip() if line.lstrip() else '\n'
                          for line_nr, line in enumerate(file)]
        return no_indent_file

    def _get_basic_indent_file(self, no_indent_file, indent_levels, insert):
        new_file = []
        for line_nr, line in enumerate(no_indent_file):
            new_file.append(insert*indent_levels[line_nr] + line
                            if line is not '\n' else '\n')

        return new_file

    def _get_absolute_indent_file(self,
                                  indented_file,
                                  absolute_indent_levels,
                                  indent_levels,
                                  insert):
        for _range, indent in absolute_indent_levels:
            prev_indent = get_indent_of_line(indented_file,
                                             _range.start.line - 1,
                                             length=False)
            prev_indent_level = indent_levels[_range.start.line - 1]
            for line in range(_range.start.line, _range.end.line):
                new_line = (prev_indent + ' '*indent +
                            insert*(indent_levels[line] - prev_indent_level) +
                            indented_file[line].lstrip())
                indented_file[line] = new_line if new_line.strip() != ''\
                    else '\n'
        return indented_file

    def get_absolute_indent_of_range(self,
                                     file,
                                     filename,
                                     ranges,
                                     encapsulators):
        """
        Gets the absolute indentation of all the encapsulators.

        :param file:            A tuple of strings.
        :param filename:        Name of file.
        :param ranges:          A dict contating ranges of various code
                                segments. Keys include: ``strings``,
                                ``comments``, ``encapsulators`` and
                                ``indent_ranges``.
        :param encapsulators:   A dict which contains specifications for
                                start and end of certain code-segments.
        :return:                A tuple of tuples with first element as the
                                range of encapsulator and second element as the
                                indent of its elements.
        """
        # Recaulculating since encapsulators will change after applying keyword
        # based indentation.
        ranges['encapsulators'] = self._calculate_encapsulators_range(
            file,
            filename,
            encapsulators,
            ranges)
        indent_of_range = []
        for encaps in ranges['encapsulators']:
            indent = get_element_indent(file, encaps)
            indent_of_range.append((encaps, indent))

        return tuple(indent_of_range)

    def get_indent_levels(self,
                          file,
                          filename,
                          indent_types,
                          ranges,
                          comments):
        """
        Gets the level of indentation of each line.

        :param file:            File that needs to be checked in the form of
                                a list of strings.
        :param filename:        Name of the file that needs to be checked.
        :param indent_types:    A dictionary with keys as start of indent and
                                values as their corresponding closing indents.
        :param ranges:          A dict contating ranges of various code
                                segments. Keys include: ``strings``,
                                ``comments``, ``encapsulators`` and
                                ``indent_ranges``.
        :param comments:        A dict containing all the types of comment
                                specifiers in a language.
        :return:                A tuple containing the levels of indentation of
                                each line.
        """
        indent_levels = []
        indent, next_indent = 0, 0
        for line in range(0, len(file)):
            indent = next_indent
            for _range in ranges['indent_ranges']:
                if _range.start.line == line + 1:
                    next_indent += 1

                first_ch = file[line].lstrip()[:1]
                if(_range.end.line == line + 1 and
                   first_ch in indent_types.values()):
                    indent -= 1
                    next_indent -= 1

                elif _range.end.line == line + 1:
                    next_indent -= 1
            indent_levels.append(indent)

        return tuple(indent_levels)

    def get_unspecified_block_range(self,
                                    file,
                                    filename,
                                    indent_specifier,
                                    ranges,
                                    comments):
        """
        Gets the range of all blocks which do not have an un-indent specifer.

        :param file:             File that needs to be checked in the form of
                                 a list of strings.
        :param filename:         Name of the file that needs to be checked.
        :param indent_specifier: A character or string indicating that the
                                 indentation should begin.
        :param ranges:           A dict contating ranges of various code
                                 segments. Keys include: ``strings``,
                                 ``comments``, ``encapsulators`` and
                                 ``indent_ranges``.
        :param comments:         A dict containing all the types of comments
                                 specifiers in a language.
        :return:                 A tuple of SourceRanges of blocks without
                                 un-indent specifiers.
        """
        specifiers = list(get_valid_sequences(
            file,
            indent_specifier,
            ranges,
            check_encapsulators=True,
            check_ending=True))

        _range = []
        for specifier in specifiers:
            current_line = specifier.line
            indent = get_indent_of_specifier(file,
                                             current_line,
                                             ranges['encapsulators'])
            unindent_line = get_first_unindent(indent,
                                               file,
                                               current_line,
                                               ranges,
                                               comments)

            if unindent_line == specifier.line:
                raise ExpectedIndentError(specifier.line)

            _range.append(SourceRange.from_values(
                filename,
                start_line=specifier.line, start_column=None,
                end_line=unindent_line, end_column=None))

        return tuple(_range)

    @staticmethod
    def get_dependencies():
        return [AnnotationBear]  # pragma: no cover


def get_indent_of_specifier(file, current_line, encapsulators):
    """
    Get indentation of the indent specifer itself.

    :param file:          A tuple of strings.
    :param current_line:  Line number of indent specifier (initial 1)
    :param encapsulators: A tuple with all the ranges of encapsulators
    :return:              Indentation of the specifier.
    """
    start = current_line
    _range = 0
    while (_range < len(encapsulators) and
           encapsulators[_range].end.line <= current_line):

        if current_line == encapsulators[_range].end.line:
            if encapsulators[_range].start.line < start:
                start = encapsulators[_range].start.line

        _range += 1

    return len(file[start - 1]) - len(file[start - 1].lstrip())


def get_first_unindent(indent,
                       file,
                       start_line,
                       ranges,
                       comments):
    """
    Get the first case of a valid unindentation.

    :param indent:          No. of spaces to check unindent against.
    :param file:            A tuple of strings.
    :param start_line:      The line from where to start searching for
                            unindent.
    :param ranges:          A dict contating ranges of various code
                            segments. Keys include: ``strings``, ``comments``,
                            ``encapsulators`` and ``indent_ranges``.
    :param comments:        A dict containing all the types of comments
                            specifiers in a language.
    :return:                The line where unindent is found (intial 0).
    """
    line_nr = start_line

    while line_nr < len(file):
        valid = True

        for comment in ranges['comments']:
            if(comment.start.line < line_nr + 1 and
               comment.end.line >= line_nr + 1):
                valid = False

            first_char = file[line_nr].lstrip()[0] if file[line_nr].strip()\
                else ''
            if first_char in comments:
                valid = False

        for encapsulator in ranges['encapsulators']:
            if(encapsulator.start.line < line_nr + 1 and
               encapsulator.end.line >= line_nr + 1):
                valid = False

        line_indent = len(file[line_nr]) - len(file[line_nr].lstrip())
        if line_indent <= indent and valid:
            return line_nr
        line_nr += 1

    return line_nr


def get_element_indent(file, encaps):
    """
    Gets indent of elements inside encapsulator.

    :param file:   A tuple of strings.
    :param encaps: SourceRange of an encapsulator.
    :return:       The number of spaces params are indented relative to
                   the start line of encapsulator.
    """
    line_nr = encaps.start.line - 1
    start_indent = get_indent_of_line(file, line_nr)
    if len(file[line_nr].rstrip()) <= encaps.start.column:
        indent = get_indent_of_line(file, line_nr + 1)
    else:
        indent = encaps.start.column

    indent = indent - start_indent if indent > start_indent else 0
    return indent


def get_indent_of_line(file, line, length=True):
    indent = len(file[line]) - len(file[line].lstrip())
    if length:
        return indent
    else:
        return file[line][:indent]
