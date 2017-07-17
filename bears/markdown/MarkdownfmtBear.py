from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GoRequirement import GoRequirement


@linter(executable='markdownfmt',
        output_format='corrected',
        result_message='Formatting can be improved.',
        use_stdin=True)
class MarkdownfmtBear:
    """
    Check and correct formatting of Markdown files using ``mardownfmt``.
    Basic checks like alignment, indendation are provided.
    Note that MarkdownfmtBear works only with pure Markdown files(shouldn't
    contain front matter like TOML, JS etc).
    """
    LANGUAGES = {'Markdown'}
    REQUIREMENTS = {GoRequirement(
                     package='github.com/shurcooL/markdownfmt')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}
    ASCIINEMA_URL = 'https://asciinema.org/a/396jhuyw1j0c1l2i9p09wlhye'
    SEE_MORE = 'https://github.com/shurcooL/markdownfmt'

    @staticmethod
    def create_arguments(filename, file, config_file):
        return list()
