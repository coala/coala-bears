from restructuredtext_lint import lint

from coalib.bears.LocalBear import LocalBear
from coalib.bears.requirements.PythonRequirement import PythonRequirement
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class reSTLintBear(LocalBear):
    LANGUAGES = {"reStructuredText"}
    REQUIREMENTS = PythonRequirement('restructuredtext_lint', '0.14.*')
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    def run(self, filename, file):
        """
        Lints reStructuredText.
        """
        content = ''.join(file)
        errors = lint(content)

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
