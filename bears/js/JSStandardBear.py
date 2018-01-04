from collections import defaultdict
import re
from subprocess import Popen, PIPE
from typing import List, Iterable, Tuple

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement
from coalib.results.Result import Result
from coalib.results.Diff import Diff


@linter(executable='standard',
        use_stdin=True,
        use_stderr=True)
class JSStandardBear:
    """
    One JavaScript Style to Rule Them All.

    No decisions to make.
    No .eslintrc, .jshintrc, or .jscsrc files to manage.
    It just works.
    """

    LANGUAGES = {'JavaScript', 'JSX'}
    REQUIREMENTS = {NpmRequirement('standard', '10')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}
    CAN_FIX = {'Formatting'}
    SEE_MORE = 'https://standardjs.com/rules.html'

    issue_regex = re.compile(
        r'\s*[^:]+:(?P<line>\d+):(?P<column>\d+):'
        r'\s*(?P<message>.+)')

    def create_arguments(self, filename, file, config_file):
        return (filename, '--verbose')

    @staticmethod
    def _get_corrected_code(old_code: List[str]) -> List[str]:
        """
        Pipes the code to JSStandard and returns the corrected code.
        """
        p = Popen(
            ('standard', '--stdin', '--fix'),
            stdin=PIPE, stdout=PIPE, stderr=PIPE)
        p.stdin.write(bytes(''.join(old_code), 'UTF-8'))
        out, err = p.communicate()
        return out.decode('UTF-8').splitlines(True)

    def _get_issues(self, stdout: str) -> Iterable[Tuple[int, str]]:
        """
        Gets the issues from the output of JSStandard.

        The issues get parsed with `self.issue_regex` and merged if they
        concern the same line.

        :param stdout: Output from which the issues get parsed.
        :return: List of tuples containing the line number and the message.
        """
        match_objects = (
            self.issue_regex.match(line) for line in stdout.splitlines())
        issues = (
            match_object.groupdict()
            for match_object in match_objects if match_object is not None)
        line_number_to_messages = defaultdict(list)
        for issue in issues:
            line_number = int(issue['line'])
            line_number_to_messages[line_number].append(issue['message'])
        return (
            (line_number, '\n'.join(messages))
            for line_number, messages
            in sorted(line_number_to_messages.items()))

    def process_output(self, output, filename, file):
        stdout, stderr = output
        corrected_code = None
        if '--fix' in stderr:
            corrected_code = self._get_corrected_code(file)
            if len(file) != len(corrected_code):
                corrected_code = None

        for line_number, message in self._get_issues(stdout):
            diff = None
            if corrected_code:
                diff = Diff(file)
                diff.modify_line(line_number, corrected_code[line_number-1])
            yield Result.from_values(
                origin=self,
                message=message,
                file=filename,
                line=line_number,
                diffs={filename: diff})
