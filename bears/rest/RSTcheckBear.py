from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Setting import typed_list


@linter(executable='rstcheck',
        use_stdout=False,
        use_stderr=True,
        output_format='regex',
        output_regex=r'.+\s?:(?P<line>\d+):\s'
                     r'(?P<message>\((?P<severity>\w+).+)',
        severity_map={'INFO': RESULT_SEVERITY.INFO,
                      'WARNING': RESULT_SEVERITY.NORMAL,
                      'ERROR': RESULT_SEVERITY.MAJOR,
                      'SEVERE': RESULT_SEVERITY.MAJOR})
class RSTcheckBear:

    """
    Check syntax of ``reStructuredText`` and code blocks
    nested within it.

    Check <https://pypi.python.org/pypi/rstcheck> for more information.
    """

    LANGUAGES = {'reStructuredText'}
    REQUIREMENTS = {PipRequirement('rstcheck', '3.1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax'}
    ASCIINEMA_URL = 'https://asciinema.org/a/8ntlaqubk2qkrn9mm0dh07rlk?speed=2'

    @staticmethod
    def create_arguments(filename, file, config_file,
                         code_block_language_ignore: list=(),
                         directive_ignore: typed_list(str)=(),
                         role_ignore: typed_list(str)=()):
        """
        :param code_block_language_ignore:
            Comma seperated list for languages of which code blocks
            should be ignored. Code block of following languages
            can be detected: ``bash``, ``c``, ``cpp``, ``json``,
            ``python``, ``rst``.
        :param directive_ignore:
             Comma separated list of directives to be ignored. Can be
             used to ignore custom directives.
        :param role_ignore:
             Comma separated list of roles to be ignored. Can be used
             to ignore custom roles.
        """
        args = ()
        if code_block_language_ignore:
            args = ('--ignore-language=' +
                    ','.join(code_block_language_ignore),)
        if directive_ignore:
            args += ('--ignore-directives=' + ','.join(directive_ignore),)
        if role_ignore:
            args += ('--ignore-roles=' + ','.join(role_ignore),)
        return args + (filename,)
