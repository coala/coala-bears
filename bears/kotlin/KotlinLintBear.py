import os

from coalib.bearlib.abstractions.Linter import linter


@linter(executable='ktlint',
        use_stderr=True,
        use_stdout=True)
class KotlinLintBear:
    """
    Lints your Kotlin Files.
    Check code for coding standards or semantical problems that might lead
    to problems in execution of the code.
    See https://ktlint.github.io for more info.
    """
    LANGUAGES = {'CSS'}
    REQUIREMENTS = {'ktlint'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax'}

    def process_output(self, output, filename, file):
        stdout, stderr = output
        dirpath = os.getcwd()
        stdout = stdout.replace(dirpath+'\\', '')
        print(stdout)

    @staticmethod
    def create_arguments(filename, file, config_file):
        return('--color', filename)
