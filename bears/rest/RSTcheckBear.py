import re

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


def _ignore_unknown(errors):
    for error in errors:
        msg = error.full_message
        res = re.search(
            r'No directive entry for "[\w|\-]+"|'
            r'No role entry for "[\w|\-]+"', msg)
        if not res:
            yield error


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
    REQUIREMENTS = {PipRequirement('rstcheck', '2.2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax'}
    ASCIINEMA_URL = 'https://asciinema.org/a/8ntlaqubk2qkrn9mm0dh07rlk?speed=2'

    @staticmethod
    def create_arguments(filename, file, config_file,
                         code_block_language_ignore: list=(),
                         ignore_directives: list=(),
                         ignore_roles: list=()):
        """
        :param code_block_language_ignore:
            Comma seperated list for languages of which code blocks
            should be ignored. Code block of following languages
            can be detected: ``bash``, ``c``, ``cpp``, ``json``,
            ``python``, ``rst``.

        :param ignore_directives:
             Comma sepereated list of directives to be ignored

        :param ignore_roles:
             Comma seperated list of roles to be ignored
        """

        args = ()

        if code_block_language_ignore:
            args = ('--ignore-language=' +
                    ','.join(code_block_language_ignore),)

        args += ((
            '--ignore-directives=' + ','
            .join(ignore_directives),)
            if ignore_directives else ()
        )

        args += ((
            '--ignore-roles=' + ','
            .join(ignore_roles),)
            if ignore_roles else ()
        )

        return args + (filename, )
