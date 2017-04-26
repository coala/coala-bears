from coalib.bears.LocalBear import LocalBear
from dependency_management.requirements.PythonImportRequirement import (
        PythonImportRequirement)
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class reSTLintBear(LocalBear):
    LANGUAGES = {'reStructuredText'}
    REQUIREMENTS = {PythonImportRequirement('restructuredtext-lint',
                                            '1.0.0',
                                            ['restructuredtext_lint.lint'])}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax'}

    def run(self, filename, file):
        """
        Lints reStructuredText.
        """
        lint = list(self.__class__.REQUIREMENTS)[0]
        lint.is_importable()
        content = ''.join(file)
        errors = lint.lint(content)

        for error in errors:
            severity = {
                1: RESULT_SEVERITY.INFO,
                2: RESULT_SEVERITY.NORMAL,
                3: RESULT_SEVERITY.MAJOR,
                4: RESULT_SEVERITY.MAJOR}.get(error.level,
                                              RESULT_SEVERITY.NORMAL)
            yield Result.from_values(
                self,
                error.message,
                file=filename,
                line=error.line,
                debug_msg=error.full_message,
                severity=severity)
