from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from dependency_management.requirements.PipRequirement import PipRequirement


@linter(executable='dennis-cmd',
        output_format='regex',
        output_regex=r'(?P<message>(?P<severity>[EW])[0-9]{3}: .*)'
                     r'\n(?P<line>[0-9]+):.*\n(?P<end_line>[0-9]+):.*',
        severity_map={'W': RESULT_SEVERITY.NORMAL,
                      'E': RESULT_SEVERITY.MAJOR})
class DennisBear:
    """
    Lints your translated PO and POT files!

    Check multiple lint rules on all the strings in the PO file
    generating a list of errors and a list of warnings.

    See http://dennis.readthedocs.io/en/latest/linting.html for
    list of all error codes.

    http://dennis.readthedocs.io/
    """

    LANGUAGES = {'po', 'pot'}
    REQUIREMENTS = {PipRequirement('dennis', '0.8'),
                    # Workaround for https://github.com/willkg/dennis/issues/91
                    PipRequirement('click', '6.6')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file, allow_untranslated=True):
        """
        :param allow_untranslated: Set to false to display unchanged
                                   translation warning.
        """
        if allow_untranslated:
            return ('lint', filename, '--excluderules', 'W302')
        else:
            return ('lint', filename)
