import json
import os

from coalib.bearlib.abstractions.Linter import linter
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from dependency_management.requirements.CargoRequirement import (
        CargoRequirement)


@linter(executable='cargo',
        global_bear=True,
        use_stdout=False,
        use_stderr=True)
class RustClippyLintBear:
    LANGUAGES = {'Rust'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {
        'Formatting',
        'Unused Code',
        'Syntax',
        'Unreachable Code',
        'Smell',
        'Code Simplification',
    }
    EXECUTABLE = 'cargo.exe' if os.name == 'nt' else 'cargo'
    REQUIREMENTS = {
        CargoRequirement('clippy')
    }
    SEVERITY_MAP = {
        'warning': RESULT_SEVERITY.NORMAL,
        'error': RESULT_SEVERITY.MAJOR,
    }

    @staticmethod
    def create_arguments(config_file):
        args = ('clippy', '--quiet', '--color', 'never',
                '--', '-Z', 'unstable-options',
                '--error-format', 'json',
                '--test')
        return args

    def process_output(self, output, filename, file):
        # Rust outputs \n's, instead of the system default.
        for line in output.split('\n'):
            if not line:
                continue
            # cargo still outputs some text, even when in quiet mode,
            # when a project does not build. We skip this, as the
            # real reason will be reported on another line.
            if line.startswith('To learn more, run the command again'):
                continue
            yield self.new_result(json.loads(line))

    def new_result(self, issue):
        span = issue['spans'][0]
        return Result.from_values(
            origin=self.__class__.__name__,
            message=issue['message'],
            file=span['file_name'],
            line=span['line_start'],
            end_line=span['line_end'],
            column=span['column_start'],
            end_column=span['column_end'],
            severity=self.SEVERITY_MAP[issue['level']])
