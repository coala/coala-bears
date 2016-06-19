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
        specifier and "}" is the end indent specifier.

        It does not however support hanging indents or absolute indents of
        any sort, also indents based on keywords are not supported yet.
        for example:

            if(something)
            does not get indented

        undergoes no change.

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
        indent_types = dict(lang_settings_dict["indent_types"])

        try:
            indent_levels = self.get_indent_levels(
                                  file, filename, indent_types, annotation_dict)
        # This happens only in case of unmatched indents.
        except UnmatchedIndentError as e:
            yield Result(self, str(e), severity=RESULT_SEVERITY.MAJOR)
            return

        insert = ' '*tab_width if use_spaces else '\t'
        new_file = []
        for line_nr, line in enumerate(file):
            # Leave out empty lines
            if line.lstrip() != '':
                new_file.append(insert*indent_levels[line_nr] +
                                line.lstrip())
            else:
                new_file.append('\n')

        if new_file != list(file):
            wholediff = Diff.from_string_arrays(file, new_file)
            for diff in wholediff.split_diff():
                yield Result(
                    self,
                    'The indentation could be changed to improve readability.',
                    severity=RESULT_SEVERITY.INFO,
                    affected_code=(diff.range(filename),),
                    diffs={filename: diff})

    def get_indent_levels(self, file, filename, indent_types, annotation_dict):
        """
        Gets the level of indentation of each line.

        :param file:            File that needs to be checked in the form of
                                a list of strings.
        :param filename:        Name of the file that needs to be checked.
        :param indent_types:    A dictionary with keys as start of indent and
                                values as their corresponding closing indents.
        :param annotation_dict: A dictionary containing sourceranges of all the
                                strings and comments within a file.
        :return:                A tuple containing the levels of indentation of
                                each line.
        """
        indent_levels = []
        ranges = self.get_specified_block_range(
                         file, filename, indent_types, annotation_dict)
        indent, next_indent = 0, 0
        for line in range(0, len(file)):
            indent = next_indent
            for _range in ranges:
                if _range.start.line == line + 1:
                    next_indent += 1
                if(_range.end.line == line + 1 and
                   (file[line].lstrip()[0] in indent_types.values())):
                    indent -= 1
                    next_indent -= 1
                elif _range.end.line == line + 1:
                    next_indent -= 1
            indent_levels.append(indent)

        return tuple(indent_levels)

    def get_specified_block_range(self,
                                  file,
                                  filename,
                                  indent_types,
                                  annotation_dict):
        """
        Gets a sourceranges of all the indentation blocks present inside the
        file.

        :param file:            File that needs to be checked in the form of
                                a list of strings.
        :param filename:        Name of the file that needs to be checked.
        :param indent_types:    A dictionary with keys as start of indent and
                                values as their corresponding closing indents.
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
        for open_indent in indent_types:
            close_indent = indent_types[open_indent]
            open_pos = list(self.get_valid_sequences(
                                     file, open_indent, annotation_dict))
            close_pos = list(self.get_valid_sequences(
                                     file, close_indent, annotation_dict))

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
                    raise UnmatchedIndentError(open_indent, close_indent)

        # Ranges are returned in the order of least nested to most nested
        # and also on the basis of which come first
        return tuple(ranges)[::-1]

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


class UnmatchedIndentError(Exception):

    def __init__(self, open_indent, close_indent):
        Exception.__init__(self, "Unmatched " + open_indent + ", " +
                           close_indent + " pair")
