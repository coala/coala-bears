from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import RESULT_SEVERITY, Result
from coalib.results.Diff import Diff
from coalib.parsing.StringProcessing.Core import (unescaped_search_for,
                                                  position_is_escaped)
from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition


class IndentationBear(LocalBear):

    def run(self,
            filename,
            file,
            language: str,
            language_family: str):
        """
        This Bear checks and corrects indentation for all languages
        which provide a mechanism for indentation start and indentation end
        for eg: ruby has 'do : end' , C has '{ : }' and so on.

        doesn't support hanging indents, keyword indents, and using spaces
        instead of tabs yet

        :param language_family: Language family to be used for indentation.
        :param language:        Language to be used for indentation.
        """
        # take settings from language
        escape_dict = {}
        indent_types = {}
        lang_settings_dict = LanguageDefinition(language, language_family)
        # escape_dict used for escaping comments and strings
        escape_dict.update(lang_settings_dict["comment delimiter"])
        escape_dict.update(lang_settings_dict["multiline comment delimiters"])
        escape_dict.update(lang_settings_dict["string delimiters"])
        indent_types.update(lang_settings_dict["indent types"])
        new_file = tuple(self.applyindent(file,
                                          indent_types,
                                          escape_dict))

        if new_file != tuple(file):
            wholediff = Diff.from_string_arrays(file, new_file)
            for diff in wholediff.split_diff():
                yield Result(
                    self,
                    'The indentation could be changed to improve readability.',
                    severity=RESULT_SEVERITY.INFO,
                    affected_code=(diff.range(filename),),
                    diffs={filename: diff})

    def applyindent(self,
                    file,
                    indent_types,
                    escape_dict):
        """
        Applies indents line by line, checking also for new indents
        that are opened within the line, while  also closing previous indents

        :param indent_types:    Dictionary containing opening and closing
                                indents of a language
        :param escape_dict:     A Dictionary containing the different types of
                                strings and comments a language supports
        :param indent:          indent level of the particular line
        :param nextindent:      indent level of the next line
        :param escape:          wether the line should be escaped and not be
                                searched for new indents
        :param nextescape:      wether the next line should be escaped
        :param abs_indent:      absolute indent of the particular line
                                for eg:
                                   func(param1,
                                        param2)
        :param next_abs_indent: list of absolute indent levels in the
                                forthcoming lines

        :param unescape_pos:    position till where the line is escaped


        :return:                An indented line
        """

        self.indent, self.nextindent = 0, 0
        self.escape, self.nextescape = False, False
        self.unescape_pos = None
        self.next_abs_indent = []
        for line_nr, line in enumerate(file, start=1):
            if self.next_abs_indent:
                # abs_indent starts with the last of the next indent
                # next_abs_indent is sorted in ascending order
                self.abs_indent = self.next_abs_indent[-1]
            else:
                self.abs_indent = None
            # indent level is set to what is calculated on the last line
            self.indent = self.nextindent
            # escape is set to what is calculated in the last line
            self.escape = self.nextescape
            # if the line is unescaped calulate in which poistion this happens
            self.unescape_pos = self.calc_escape_end(line, escape_dict)
            # change the nextindent as per requirements of the line
            self.get_indent(line, indent_types, escape_dict)
            # if previous indents are closed in this line reduce the indent
            self.close_indents_in_this_line(line, indent_types)
            stripped = line.lstrip()
            # if the line is not to be absolutely indented
            if self.abs_indent is None:
                if stripped:
                    self.check_abs_indents(stripped, escape_dict)
                    yield self.indent*'\t' + stripped
                else:
                    yield line
            else:
                if stripped:
                    line_with_spaces = (self.abs_indent+1)*' '+stripped
                    indented_line = self.indent*'\t' + line_with_spaces
                    self.check_abs_indents(indented_line, escape_dict)
                    yield indented_line
                else:
                    yield line

    # An escape is a string or a comment, indents within which we should ignore
    def not_within_escape_pos(self, line, istring, escape_dict):
        """
        Calculates all the positions of a string in a line, where
        the string is not enclosed within a string or a comment

        :param line:    line in which the string has to be searched
        :param istring: The string needed to be searched
        :escape_dict:   Dictionary containing all string and comment types

        :return:        A list containing all of the positions of
                        the string that aren't within a string or a comment
        """
        # The list containing all valid occurances of istring
        found = []
        istring_pos = line.find(istring)
        # unescape_pos not None means this line is not escaped
        if self.unescape_pos is not None:
            pos = self.unescape_pos+1
        else:
            pos = -1
        # list that will contain all the closing positions
        # of open strings and comments
        close_list = []
        while pos < len(line) and pos > -1:
            # escape_str is the string or comment starting at position=pos
            escape_str = in_dict(line, pos, escape_dict)
            if escape_str:
                # escape_end is the closing tag of escape_str
                escape_end = escape_dict[escape_str]
                # if escape has no closing tag
                if not escape_end:
                    return found
                # find position of closing tag
                temp_pos = -1
                close_list = list(unescaped_search_for(escape_end, line))
                # Calculates the next closing of opened escape
                close_list = [i for i in close_list if i.start() > pos]
                if close_list:
                    temp_pos = close_list[0].start()
                    close_list.pop(0)

                pos = temp_pos
                # if comment or string does not close in that line
                if pos == -1:
                    self.nextescape = True
                    self.escape_str = escape_str
                    return found
            # If no escape is opened and still we find an indent type
            if istring_pos == pos:
                found.append(pos)

            elif istring_pos < pos:
                istring_pos = line.find(istring, pos)
                if istring_pos == pos:
                    found.append(pos)
            pos += 1
        return found

    def get_indent(self, line, indent_types, escape_dict):
        """
        Checks if there are any indents that are not closed in the same line
        """
        for indent in indent_types:
            op_indnt_pos = self.not_within_escape_pos(line, indent, escape_dict)
            cl_indnt_pos = self.not_within_escape_pos(line,
                                                      indent_types[indent],
                                                      escape_dict)

            if op_indnt_pos:
                open_indents = self.check_indents(op_indnt_pos, cl_indnt_pos)
                self.nextindent += len(open_indents)

            if cl_indnt_pos:
                clos_indents = self.check_indents(cl_indnt_pos,
                                                  op_indnt_pos,
                                                  closing=True)
                self.nextindent -= len(clos_indents)

    def check_abs_indents(self, line, escape_dict):
        """
        checks if there are any paranthesis opened and not closed within
        the same line, if there are, their positons get appended to
        the next_abs_indent list, also reduces the abs indent if
        paranthesis from previous lines were closed
        """
        brackets_open = self.not_within_escape_pos(line,
                                                   "(",
                                                   escape_dict)
        brackets_closed = self.not_within_escape_pos(line,
                                                     ")",
                                                     escape_dict)
        if brackets_open:
            br_open = self.check_indents(brackets_open, brackets_closed)
            self.next_abs_indent += br_open

        if brackets_closed:
            br_close = self.check_indents(
                brackets_closed, brackets_open, closing=True)
            for bracket in br_close:
                self.next_abs_indent.pop()

    def check_indents(self, to_check, against, closing=False):
        """
        takes a list of positions of open and closed indents
        and returns a list of indents opend in the same line,
        or indents to be closed of previous lines.
        for eg :
            {}{}{{} : has one open indent
            }{{{}}} : has one open closing_indent

        :param to_check: a list containing the indents which has to be
                         checked for open, eg: a list of positions of '{'
                         or a list of positions of '}'
                         depending on what has to be checked
        :param against:  a list containing the indents which close the indents
                         in the to_check list. If to_chek is a list of positions
                         of '{' then against is a list of positions of '}'.
        :param closing:  A boolean to check wether to check for open
                         indents or open closing_indents

        :return:         the number of open indents or open closing_indents in
                         a line
        """
        to_check.sort(reverse=closing)
        against.sort(reverse=closing)
        merged = sorted(to_check + against, reverse=closing)
        indent_level = []
        for i in merged:
            if i in to_check:
                indent_level.append(i)
            elif i in against and indent_level:
                indent_level.pop()
        return indent_level

    def calc_escape_end(self, line, escape_dict):
        """
        calculates the position where a multiline string or
        comment is closed

        :return:    None if escape doesn't end in this line,
                    -1 if line was not escaped in the first place,
                    and an integer pointing to the position of end of string
                    or comment if it is found in the line
        """
        if self.escape:
            if escape_dict[self.escape_str] not in line:
                return None
            else:
                self.escape = False
                self.nextescape = False
                return line.find(escape_dict[self.escape_str])
        return -1

    def close_indents_in_this_line(self, line, indent_types):
        """
        if a closing_indent is present at the start of a line
        then reduces the indent of that line
        """
        for indent_close in indent_types.values():
            stripped = line.lstrip()
            while stripped.startswith(indent_close):
                self.indent -= 1
                stripped = stripped[len(indent_close):].lstrip()


def in_dict(line, pos, dict):
    """
    checks if any of the keys of the given dict is present at the
    at a particular position in the line

    :param pos:  The position where keys of dict are to be searched
    :param line: The line which is to be searched
    :param dict: the dict who's keys are to be searched
    """
    if position_is_escaped(line, pos):
        return None
    for i in dict.keys():
        if line.find(i) == pos:
            return i
    return None
