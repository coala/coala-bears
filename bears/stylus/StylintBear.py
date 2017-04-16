from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.NpmRequirement import NpmRequirement


@linter(executable='stylint',
        output_format='regex',
        output_regex=r'(?P<line>\d+):?(?P<column>\d+)?\s+.*?'
                     r'(?P<severity>error|warning)\s+(?P<message>.+?)'
                     r'(?:  .*|\n|$)')
class StylintBear:
    """
    Attempts to catch little mistakes (duplication of rules for instance) and
    enforces a code style guide on Stylus (a dynamic stylesheet language
    with the ``.styl`` extension that is compiled into CSS) files.

    The ``StylintBear`` is able to catch following problems:
    - Duplication of rules
    - Mixed spaces and tabs
    - Unnecessary brackets
    - Missing colon between property and value
    - Naming conventions
    - Trailing whitespace
    - Consistent quotation style
    - Use of extra spaces inside parenthesis
    - Naming convention when declaring classes, ids, and variables
    - Unnecessary leading zeroes on decimal points
    - Checks if a property is valid CSS or HTML
    """

    LANGUAGES = {'Stylus'}
    REQUIREMENTS = {NpmRequirement('stylint', '1.5.9')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax', 'Redundancy'}
    SEE_MORE = 'https://github.com/SimenB/stylint'

    @staticmethod
    def create_arguments(filename, file, config_file, stylint_config: str=''):
        """
        :param stylint_config:
            The location of the ``.stylintrc`` config file.
        """
        if stylint_config:
            return '--config', stylint_config, filename
        else:
            return filename,
