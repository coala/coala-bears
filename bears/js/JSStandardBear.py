from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(executable='standard',
        output_format='regex',
        output_regex=r'\s*[^:]+:(?P<line>\d+):(?P<column>\d+):'
                     r'\s*(?P<message>.+)')
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

    def create_arguments(self, filename, file, config_file):
        return (filename, '--verbose')
