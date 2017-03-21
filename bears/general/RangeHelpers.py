from coala_utils.string_processing.Core import unescaped_search_for
from coalib.results.AbsolutePosition import AbsolutePosition
from coalib.results.SourceRange import SourceRange

from bears.general.CustomExceptions import (UnmatchedIndentError,
                                            ExpectedIndentError)


def get_specified_block_range(file,
                              filename,
                              open_specifier,
                              close_specifier,
                              ranges):
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
    :param ranges:          A dict contating ranges of various code
                            segments. Keys include: ``strings``, ``comments``,
                            ``encapsulators`` and ``indent_ranges``.
    :return:                A tuple whith the first source range being
                            the range of the outermost indentation while
                            last being the range of the most
                            nested/innermost indentation.
                            Equal level indents appear in the order of
                            first encounter or left to right.
    """
    indent_ranges = []

    open_pos = list(get_valid_sequences(
        file, open_specifier, ranges))
    close_pos = list(get_valid_sequences(
        file, close_specifier, ranges))

    number_of_encaps = len(open_pos)
    if number_of_encaps != len(close_pos):
        raise UnmatchedIndentError(open_specifier, close_specifier)

    if number_of_encaps == 0:
        return ()

    stack = []
    text = ''.join(file)
    open_counter = close_counter = position = 0
    op_limit = cl_limit = False
    for position in range(len(text)):
        if not op_limit and open_pos[open_counter].position == position:
            stack.append(open_pos[open_counter])
            open_counter += 1
            if open_counter == number_of_encaps:
                op_limit = True

        if not cl_limit and close_pos[close_counter].position == position:
            try:
                op = stack.pop()
            except IndexError:
                raise UnmatchedIndentError(open_specifier,
                                           close_specifier)
            indent_ranges.append(SourceRange.from_values(
                filename,
                start_line=op.line,
                start_column=op.column,
                end_line=close_pos[close_counter].line,
                end_column=close_pos[close_counter].column))
            close_counter += 1
            if close_counter == number_of_encaps:
                cl_limit = True
    return tuple(indent_ranges)


def get_valid_sequences(file,
                        sequence,
                        ranges,
                        check_encapsulators=False,
                        check_ending=False,
                        keyword=False):
    """
    A vaild sequence is a sequence that is outside of comments or strings.

    :param file:                File that needs to be checked in the form of
                                a list of strings.
    :param sequence:            Sequence whose validity is to be checked.
    :param ranges:              A dict contating ranges of various code
                                segments.
    :param check_encapsulators: Check whether a sequence is inside an
                                encapsulator.
    :param check_ending:        Check whether sequence falls at the end of the
                                line.
    :param keyword:             A boolean which filters occurrances of sequence
                                which are not actually keywords.
    :return:                    A tuple of AbsolutePosition's of all occurances
                                of sequence outside of string's and comments.
    """
    file_string = ''.join(file)
    # tuple since order is important
    sequence_positions = tuple()

    for sequence_match in unescaped_search_for(sequence, file_string):
        valid = True
        sequence_position = AbsolutePosition(
                                file, sequence_match.start())
        sequence_line_text = file[sequence_position.line - 1]

        # ignore if within string
        for string in ranges['strings']:
            if(gt_eq(sequence_position, string.start) and
               lt_eq(sequence_position, string.end)):
                valid = False

        # ignore if within comments
        for comment in ranges['comments']:
            if(gt_eq(sequence_position, comment.start) and
               lt_eq(sequence_position, comment.end)):
                valid = False

            if(comment.start.line == sequence_position.line and
                    comment.end.line == sequence_position.line and
                    check_ending):
                sequence_line_text = sequence_line_text[
                    :comment.start.column - 1] + sequence_line_text[
                    comment.end.column-1:]

        if check_encapsulators:
            valid = not any(gt_eq(sequence_position, encapsulator.start)
                            and lt_eq(sequence_position, encapsulator.end)
                            for encapsulator in ranges['encapsulators'])
        if not sequence_line_text.rstrip().endswith(':') and check_ending:
            valid = False

        if(keyword and
                (sequence_position.column - 2 != -1 or
                 file[sequence_position.line - 1]
                 [sequence_position.column - 2].strip() == '')):
            valid = False
            for encapsulator in ranges['encapsulators']:
                if encapsulator.start.line == sequence_position.line:
                    if(sequence_position.column + len(sequence) <=
                            encapsulator.start.column and
                            file[sequence_position.line - 1]
                                [sequence_position.column + len(sequence) - 1:
                                 encapsulator.start.column - 1].strip() == ''):
                        valid = True
            if (file[sequence_position.line - 1]
                    [sequence_position.column + len(sequence) - 1].strip()
                    == ''):
                valid = True

        if valid:
            sequence_positions += (sequence_position,)

    return sequence_positions


# TODO remove these once https://github.com/coala-analyzer/coala/issues/2377
# gets a fix
def lt_eq(absolute, source):
    if absolute.line == source.line:
        return absolute.column <= source.column

    return absolute.line < source.line


def gt_eq(absolute, source):
    if absolute.line == source.line:
        return absolute.column >= source.column

    return absolute.line > source.line
