import re
from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(executable='prettier',
        use_stdout=True,
        use_stderr=True)
class PrettierLintBear:
    """
    Formats JavaScript, JSX, Flow, TypeScript, CSS, Less, SCSS, JSON, GraphQL,
    Vue, Markdown files according to opinionated code format
    using ``prettier``.
    """
    LANGUAGES = {'JavaScript', 'TypeScript', 'CSS', 'Less',
                 'SCSS', 'Vue', 'JSON', 'GraphQL', 'Markdown'}
    REQUIREMENTS = {NpmRequirement('prettier', '1.9.2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Consistency', 'Correctness', 'Whitespace',
                  'Parentheses', 'Strings', 'Empty lines',
                  'Multi-line objects'}
    CAN_FIX = {'Formatting'}
    SEE_MORE = 'https://prettier.io/'

    regex = re.compile(r'L(?P<line>\d+)C(?P<column>\d+): (?P<message>.*)')

    def process_output(self, output, filename, file):
        stdout, stderr = output
        yield from self.process_output_corrected(stdout, filename, file)
        yield from self.process_output_regex(stderr, filename, file,
                                             self.regex)

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
