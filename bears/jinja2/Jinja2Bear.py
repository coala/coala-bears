import re

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result, RESULT_SEVERITY
from coalib.results.Diff import Diff


def generate_spacing_diff(file, filename, line, line_number,
                          match_object, required_spacing):
    """
    Generate a diff for incorrectly spaced control or variable tags.

    :param match_object:     A Match object containing the groups ``open``,
                             ``close`` containing the opening and closing
                             delimiters of a Jinja2 tag and ``content``
                             containing everything in between.
    :param required_spacing: The number of spaces expected after the ``open``
                             delimiter and before the ``close`` delimiter
    """
    diff = Diff(file)

    content_before = line[:match_object.start('open')]
    content_after = line[match_object.end('close'):]

    spacing = ' ' * required_spacing
    replacement = (
        '{before}{open}{spacing}{content}{spacing}{close}{after}'.format(
            before=content_before,
            spacing=spacing,
            after=content_after,
            content=match_object.group('content').strip(),
            open=match_object.group('open'),
            close=match_object.group('close')))
    diff.change_line(
        line_number,
        line,
        replacement)
    return {filename: diff}


def generate_label_diff(file, filename, line, line_number,
                        match_object, expected_label):
    """
    Generates a diff for a missing or wrong control loop end label.
    Missing labels will be added, wrong ones replaced, content after the
    label will be left untouched.


    :param match_object:   A Match object containing the groups ``close``
                           containing the closing delimiters of a control
                           end tag and the optional group ``label``
                           containing the end tag label.
    :param expected_label: The expected label for that control block.

    """
    diff = Diff(file)

    content_before = line[:match_object.end('close')]

    suffix_start = match_object.end('close')
    # if a label is there, we cut it out, by starting the kept suffix after it
    if match_object.group('label') is not None:
        suffix_start = match_object.end('label')

    content_after = line[suffix_start:]

    replacement = '{before}{label}{after}'.format(
        before=content_before,
        after=content_after,
        label=expected_label
    )
    diff.change_line(
        line_number,
        line,
        replacement)
    return {filename: diff}


def has_required_spacing(string, required_spacing):
    """
    Checks if a string has the required amount of spaces
    on each side.

    :param string:           The string which is to be checked.
    :param required_spacing: The number of spaces expected on both
                             sides of the string.
    :return:                 True if the string has the required
                             number of spaces on both sides, False
                             otherwise.

    >>> has_required_spacing("  foo  ", 2)
    True
    >>> has_required_spacing(" foo", 1)
    False
    """
    leading_spaces = len(string) - len(string.lstrip(' '))
    trailing_spaces = len(string) - len(string.rstrip(' '))

    return (
        leading_spaces == required_spacing
        and trailing_spaces == required_spacing)


class Jinja2Bear(LocalBear):
    LANGUAGES = {'Jinja2'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/azi6u1gcxutoxn0l7xpu4pljp'
    CAN_DETECT = {'Syntax'}
    CAN_FIX = {'Formatting', 'Documentation'}

    VARIABLE_REGEX = re.compile(
        r'(?P<open>{{)(?P<content>.*?)(?P<close>}})')
    CONTROL_START_REGEX = re.compile(
        r'(?P<open>{%)(?P<content>\s*(for|if).*?)(?P<close>%})')
    CONTROL_END_REGEX = re.compile(
        r'(?P<open>{%)(?P<content>\s*end(for|if)\s*?)'
        r'(?P<close>%})(?P<label>{#.*?#})?')

    def handle_control_spacing_issue(self, file, filename, line, line_number,
                                     control_spacing, match_object):
        """
        Handles incorrectly spaced control tags (if and for),
        both start and end tags

        :param control_spacing: The number of spaces placed around control tags
                                as required by the settings.
        :param match_object:    A Match object containing the groups ``open``,
                                ``close`` containing the opening and closing
                                delimiters of a Jinja2 tag and ``content``
                                containing everything in between.
        """
        diff = generate_spacing_diff(
            file, filename, line, line_number, match_object, control_spacing)
        return Result.from_values(
            origin=self,
            message='Control blocks should be spaced with '
                    '`{0}` spaces on each side.'.format(
                        control_spacing),
            file=filename,
            line=line_number,
            column=match_object.start(0) + 1,
            end_line=line_number,
            end_column=match_object.end(0) + 1,
            diffs=diff)

    def check_for_variable_spacing_issues(self,
                                          file,
                                          filename,
                                          line,
                                          line_number,
                                          variable_spacing):
        """
        Checks any variable in the given line for spacing issues.
        Yields a Result for each issue found.

        :param file:
            The content of the file currently being inspected.
        :param filename:
            The name of the file currently being inspected.
        :param line:
            The content of the line currently being inspected.
        :param line_number:
            The current line number.
        :param variable_spacing:
            The number of spaces required on each side of a variable tag.
        """
        for m in self.VARIABLE_REGEX.finditer(line):
            match = m.group('content')
            if not has_required_spacing(match, variable_spacing):
                diff = generate_spacing_diff(
                    file, filename, line, line_number, m,
                    variable_spacing)
                yield Result.from_values(
                    origin=self,
                    message='Variable blocks should be spaced with '
                            '`{0}` spaces on each side.'.format(
                                variable_spacing),
                    file=filename,
                    line=line_number,
                    column=m.start(0) + 1,
                    end_line=line_number,
                    end_column=m.end(0) + 1,
                    diffs=diff)

    def check_control_start_tags(self,
                                 file,
                                 filename,
                                 line,
                                 line_number,
                                 control_spacing):
        """
        Checks any control start tag in the given line for spacing issues
        and puts the expected label on the ``control_stack``
        Yields a Result for each issue found.

        :param file:
            The content of the file currently being inspected.
        :param filename:
            The name of the file currently being inspected.
        :param line:
            The content of the line currently being inspected.
        :param line_number:
            The current line number.
        :param control_spacing:
            The number of spaces required on each side of a control tag.
        """
        for m in self.CONTROL_START_REGEX.finditer(line):
            # build the label which is expected at the end of this block
            end_label = '{{#{spacing}{content}{spacing}#}}'.format(
                content=m.group('content').strip(),
                spacing=' ' * control_spacing)
            self.control_stack.append((end_label, line_number))

            # check for spacing issues with this tag
            if not has_required_spacing(m.group('content'), control_spacing):
                yield self.handle_control_spacing_issue(
                    file, filename, line, line_number, control_spacing, m)

    def check_control_end_tags(self,
                               file,
                               filename,
                               line,
                               line_number,
                               control_spacing):
        """
        Checks any control end tag in the given line for spacing issues,
        missing/wrong labels or missing corresponding opening tag.
        Yields a Result for each issue found.

        :param file:
            The content of the file currently being inspected.
        :param filename:
            The name of the file currently being inspected.
        :param line:
            The content of the line currently being inspected.
        :param line_number:
            The current line number.
        :param control_spacing:
            The number of spaces required on each side of a control tag.
        """
        for m in self.CONTROL_END_REGEX.finditer(line):
            label = m.group('label')
            try:
                expected_label, start_in_line = self.control_stack.pop()
            except IndexError:
                # an end tag without an opening tag
                yield Result.from_values(
                    origin=self,
                    message='Control end tag has no corresponding start',
                    file=filename,
                    line=line_number,
                    column=m.start(0) + 1,
                    end_line=line_number,
                    end_column=m.end(0) + 1,
                    severity=RESULT_SEVERITY.MAJOR)
                # Continue to next line as we've detected a syntax error
                # and label checking can give false results
                continue

            # check for spacing issues with this tag
            if not has_required_spacing(m.group('content'), control_spacing):
                yield self.handle_control_spacing_issue(
                    file, filename, line, line_number, control_spacing, m)

            # yield results for incorrect or missing end labels
            if label is None and line_number != start_in_line:
                diff = generate_label_diff(
                    file, filename, line, line_number, m, expected_label)
                yield Result.from_values(
                    origin=self,
                    message='Unlabeled control end tag',
                    file=filename,
                    line=line_number,
                    column=m.start(0) + 1,
                    end_line=line_number,
                    end_column=m.end(0) + 1,
                    diffs=diff)
            elif label != expected_label and line_number != start_in_line:
                diff = generate_label_diff(
                    file, filename, line, line_number, m, expected_label)
                yield Result.from_values(
                    origin=self,
                    message='End tag label does not match expected label',
                    file=filename,
                    line=line_number,
                    column=m.start('label') + 1,
                    end_line=line_number,
                    end_column=m.end('label') + 1,
                    diffs=diff)

    def check_for_empty_control_stack(self, filename):
        """
        Checks if the control stack is empty and yields a Result for each
        item left on the stack.

        :param filename: The name of the file currently being inspected.
        """
        if len(self.control_stack) > 0:
            for (_, line_number) in self.control_stack:
                yield Result.from_values(
                    origin=self,
                    message='Control start tag has no corresponding end',
                    file=filename,
                    line=line_number,
                    severity=RESULT_SEVERITY.MAJOR)

    def run(self,
            filename,
            file,
            variable_spacing: int=1,
            control_spacing: int=1):
        """
        Check Jinja2 templates for syntax, formatting and documentation issues.
        The following aspects are being looked at:

        * Variable spacing:
            Variable tags should be padded with one space on each side, like
            this: ``{{ var_name }}``. This can be set to any number of spaces
            via the setting variable_spacing. Malformatted variable tags are
            detected and fixes suggested.
        * Control spacing:
            Like variable spacing, but for control blocks, i.e. if and for
            constructs. Looks at both start and end block.
        * Control labels:
            It is good practice to label the end of an ``if`` or ``for``
            construct with a comment equal to the content of the start,
            like so::

                {% for x in y %}
                  do something
                {% endfor %}{# for x in y %}

            Mising or differing labels are detected and fixes suggested.
            Constructs with start and end on the same line are being ignored.
        * unbalanced blocks:
            Each opening tag for a ``for`` or ``if`` construct must be closed
            by a corresponding end tag. An unbalanced number of opening and
            closing tags is invalid syntax and will be reported with
            MAJOR severity by the bear.


        :param variable_spacing:
            The number of spaces a variable block should be spaced with.
            Default is 1.
        :param control_spacing:
            The number of spaces a control block should be spaced with.
            Default is 1.
        """

        # Whenever a control construct starts a tuple of the
        # expected end label and line number are put on this stack.
        # Whenever an end tag is encountered the last item added is popped.
        self.control_stack = []

        for line_number, line in enumerate(file, start=1):

            yield from self.check_for_variable_spacing_issues(
                file, filename, line, line_number, variable_spacing)

            yield from self.check_control_start_tags(
                file, filename, line, line_number, control_spacing)

            yield from self.check_control_end_tags(
                file, filename, line, line_number, control_spacing)

        # We've reached the end of the file.
        # Check if all control blocks have been closed
        yield from self.check_for_empty_control_stack(filename)
