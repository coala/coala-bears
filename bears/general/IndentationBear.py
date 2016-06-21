from coalib.bears.LocalBear import LocalBear
from coalib.parsing.StringProcessing.Core import unescaped_search_for
from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition
from coalib.results.SourceRange import SourceRange
from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.results.AbsolutePosition import AbsolutePosition
from coalib.results.Diff import Diff

from bears.general.AnnotationBear import AnnotationBear
from bears.general.AnnotationBear import starts_within_ranges


class IndentationBear(LocalBear):

    def run(self,
            filename,
            file,
            dependency_results: dict,
            language: str,
            use_spaces: bool=True,
            tab_width: int=4,
            coalang_dir: str=None):
        """
        It is a generic indent bear, which looks for a start and end
        indent specifier, example: ``{ : }`` where "{" is the start indent
        specifier and "}" is the end indent specifier. If the end-specifier
        is not given, this bear looks for unindents within the code to correctly
        figure out indentation.

        It does not however support hanging indents or absolute indents of
        any sort, also indents based on keywords are not supported yet.
        for example:

            if(something)
            does not get indented

        undergoes no change.

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
        :param tab_width:
            No. of spaces to insert for indentation.
            Only Applicable if use_spaces is False.
        :param coalang_dir:
            Full path of external directory containing the coalang
            file for language.
        """
        lang_settings_dict = LanguageDefinition(
            language, coalang_dir=coalang_dir)
        annotation_dict = dependency_results[AnnotationBear.name][0].contents
        # sometimes can't convert strings with ':' to dict correctly
        if ':' in list(lang_settings_dict["indent_types"]):
            indent_types = dict(lang_settings_dict["indent_types"])
            indent_types[':'] = ''
        else:
            indent_types = dict(lang_settings_dict["indent_types"])

        encapsulators = (dict(lang_settings_dict["encapsulators"]) if
                         "encapsulators" in lang_settings_dict else {})

        encaps_pos = []
        for encapsulator in encapsulators:
            encaps_pos += self.get_specified_block_range(
                file, filename,
                encapsulator, encapsulators[encapsulator],
                annotation_dict)
        encaps_pos = tuple(sorted(encaps_pos, key=lambda x: x.start.line))

        comments = dict(lang_settings_dict["comment_delimiter"])
        comments.update(
            dict(lang_settings_dict["multiline_comment_delimiters"]))

        try:
            indent_levels = self.get_indent_levels(
                file, filename,
                indent_types, annotation_dict, encaps_pos, comments)
        # This happens only in case of unmatched indents or ExpectedIndentError.
        except (UnmatchedIndentError, ExpectedIndentError) as e:
            yield Result(self, str(e), severity=RESULT_SEVERITY.MAJOR)
            return

        insert = ' '*tab_width if use_spaces else '\t'
        no_indent_file = [line.lstrip() if line.lstrip() else "\n"
                          for line_nr, line in enumerate(file)]

        new_file = []
        for line_nr, line in enumerate(no_indent_file):
            new_file.append(insert*indent_levels[line_nr] + line
                            if line is not "\n" else "\n")

        if new_file != list(file):
            wholediff = Diff.from_string_arrays(file, new_file)
            for diff in wholediff.split_diff():
                yield Result(
                    self,
                    'The indentation could be changed to improve readability.',
                    severity=RESULT_SEVERITY.INFO,
                    affected_code=(diff.range(filename),),
                    diffs={filename: diff})

    def get_indent_levels(self,
                          file,
                          filename,
                          indent_types,
                          annotation_dict,
                          encapsulators,
                          comments):
        """
        Gets the level of indentation of each line.

        :param file:            File that needs to be checked in the form of
                                a list of strings.
        :param filename:        Name of the file that needs to be checked.
        :param indent_types:    A dictionary with keys as start of indent and
                                values as their corresponding closing indents.
        :param annotation_dict: A dictionary containing sourceranges of all the
                                strings and comments within a file.
        :param encapsulators:   A tuple of sourceranges of all encapsulators of
                                a language.
        :param comments:        A dict containing all the types of comment
                                specifiers in a language.
        :return:                A tuple containing the levels of indentation of
                                each line.
        """
        ranges = []
        for indent_specifier in indent_types:
            if indent_types[indent_specifier]:
                ranges += self.get_specified_block_range(
                    file, filename,
                    indent_specifier, indent_types[indent_specifier],
                    annotation_dict)
            else:
                ranges += self.get_unspecified_block_range(
                    file, filename,
                    indent_specifier, annotation_dict, encapsulators, comments)

        ranges = sorted(ranges, key=lambda x: x.start.line)
        indent_levels = []
        indent, next_indent = 0, 0
        for line in range(0, len(file)):
            indent = next_indent
            for _range in ranges:
                if _range.start.line == line + 1:
                    next_indent += 1

                first_ch = file[line].lstrip()[0] if file[line].lstrip() else ""
                if(_range.end.line == line + 1 and
                   first_ch in indent_types.values()):
                    indent -= 1
                    next_indent -= 1

                elif _range.end.line == line + 1:
                    next_indent -= 1
            indent_levels.append(indent)

        return tuple(indent_levels)

    def get_specified_block_range(self,
                                  file,
                                  filename,
                                  open_specifier,
                                  close_specifier,
                                  annotation_dict):
        """
        Gets a sourceranges of all the indentation blocks present inside the
        file.

        :param file:            File that needs to be checked in the form of
                                a list of strings.
        :param filename:        Name of the file that needs to be checked.
        :param open_specifier:  A character or string indicating that the
                                block has begun.
        :param close_specifier: A character or string indicating that the block
                                has ended.
        :param annotation_dict: A dictionary containing sourceranges of all the
                                strings and comments within a file.
        :return:                A tuple whith the first source range being
                                the range of the outermost indentation while
                                last being the range of the most
                                nested/innermost indentation.
                                Equal level indents appear in the order of
                                first encounter or left to right.
        """
        ranges = []

        open_pos = list(self.get_valid_sequences(
            file, open_specifier, annotation_dict))
        close_pos = list(self.get_valid_sequences(
            file, close_specifier, annotation_dict))

        to_match = len(open_pos) - 1
        while to_match >= 0:
            close_index = 0
            while close_index < len(close_pos):
                if(open_pos[to_match].position
                   <= close_pos[close_index].position):
                    ranges.append(
                        SourceRange.from_absolute_position(
                            filename,
                            open_pos[to_match],
                            close_pos[close_index]))
                    close_pos.remove(close_pos[close_index])
                    open_pos.remove(open_pos[to_match])
                    to_match -= 1
                    break
                close_index += 1
            if((len(close_pos) == 0 and to_match != -1) or
               (len(close_pos) != 0 and to_match == -1)):
                # None to specify unmatched indents
                raise UnmatchedIndentError(open_specifier, close_specifier)

        # Ranges are returned in the order of least nested to most nested
        # and also on the basis of which come first
        return tuple(ranges)[::-1]

    def get_unspecified_block_range(self,
                                    file,
                                    filename,
                                    indent_specifier,
                                    annotation_dict,
                                    encapsulators,
                                    comments):
        """
        :param file:             File that needs to be checked in the form of
                                 a list of strings.
        :param filename:         Name of the file that needs to be checked.
        :param indent_specifier: A character or string indicating that the
                                 indentation should begin.
        :param annotation_dict: A dictionary containing sourceranges of all the
                                strings and comments within a file.
        :param encapsulators:   A tuple of sourceranges of all encapsulators of
                                a language.
        :param comments:        A dict containing all the types of comments
                                specifiers in a language.
        """
        specifiers = list(self.get_valid_sequences(
            file, indent_specifier, annotation_dict))
        _range = []
        for specifier in specifiers:
            current_line = specifier.line
            indent = get_indent_of_specifier(file, current_line, encapsulators)
            unindent_line = get_first_unindent(indent,
                                               file,
                                               current_line,
                                               annotation_dict,
                                               encapsulators,
                                               comments)

            if unindent_line == specifier.line:
                raise ExpectedIndentError(specifier.line)

            _range.append(SourceRange.from_values(
                filename,
                start_line=specifier.line, start_column=None,
                end_line=unindent_line, end_column=None))

        return tuple(_range)

    @staticmethod
    def get_valid_sequences(file, sequence, annotation_dict):
        """
        A vaild sequence is a sequence that is outside of comments or strings.

        :param file:            File that needs to be checked in the form of
                                a list of strings.
        :param sequence:        Sequence whose validity is to be checked.
        :param annotation_dict: A dictionary containing sourceranges of all the
                                strings and comments within a file.
        :return:                A tuple of AbsolutePosition's of all occurances
                                of sequence outside of string's and comments.
        """
        file_string = ''.join(file)
        # tuple since order is important
        sequence_positions = tuple()

        for sequence_match in unescaped_search_for(sequence, file_string):
            valid = True
            sequence_position = AbsolutePosition(
                                    file, sequence_match.start())

            # ignore if within string
            for string in annotation_dict['strings']:
                if(sequence_position >= string.start and
                   sequence_position <= string.end):
                    valid = False

            # ignore if within comments
            for comment in annotation_dict['comments']:
                if(sequence_position >= comment.start and
                   sequence_position <= comment.end):
                    valid = False

            if valid:
                sequence_positions += (sequence_position,)

        return sequence_positions

    @staticmethod
    def get_dependencies():
        return [AnnotationBear]  # pragma: no cover


def get_indent_of_specifier(file, current_line, encapsulators):
    """
    get indentation of the indent specifer itself.

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
            start = encapsulators[_range].start.line

        _range += 1

    return len(file[start - 1]) - len(file[start - 1].lstrip())


def get_first_unindent(indent,
                       file,
                       start_line,
                       annotation_dict,
                       encapsulators,
                       comments):
    """
    get the first case of a valid unindentation.

    :param indent:          No. of spaces to check unindent against.
    :param file:            A tuple of strings.
    :param start_line:      The line from where to start searching for unindent.
    :param annotation_dict: A dictionary containing sourceranges of all the
                            strings and comments within a file.
    :param encapsulators:
    :param comments:        A dict containing all the types of comments
                            specifiers in a language.
    :return:                The line where unindent is found (intial 0).
    """
    line_nr = start_line

    while line_nr < len(file):
        valid = True

        for comment in annotation_dict["comments"]:
            if(comment.start.line < line_nr + 1 and
               comment.end.line >= line_nr + 1):
                valid = False

            first_char = file[line_nr].lstrip()[0]
            if first_char in comments:
                valid = False

        for encapsulator in encapsulators:
            if(encapsulator.start.line < line_nr + 1 and
               encapsulator.end.line >= line_nr + 1):
                valid = False

        line_indent = len(file[line_nr]) - len(file[line_nr].lstrip())
        if line_indent <= indent and valid:
            return line_nr
        line_nr += 1

    return line_nr


class ExpectedIndentError(Exception):

    def __init__(self, line):
        Exception.__init__(self, "Expected indent after line: " + str(line))


class UnmatchedIndentError(Exception):

    def __init__(self, open_indent, close_indent):
        Exception.__init__(self, "Unmatched " + open_indent + ", " +
                           close_indent + " pair")
