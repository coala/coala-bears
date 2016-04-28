from coalib.parsing.StringProcessing import escape

from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='julia',
        output_format='regex',
        output_regex=r'.+:(?P<line>\d+) (?P<severity>.)\d+ (?P<message>.*)',
        severity_map={'E': RESULT_SEVERITY.MAJOR,
                      'W': RESULT_SEVERITY.NORMAL,
                      'I': RESULT_SEVERITY.INFO},
        prerequisite_check_command=('julia', '-e', 'import Lint.lintfile'),
        prerequisite_check_fail_message='Lint package not installed. Run '
                                        '`Pkg.add("Lint")` from Julia to '
                                        'install Lint.')
class JuliaLintBear:
    """
    Provide analysis related to common bugs and potential issues in Julia like
    dead code, undefined variable usage, duplicate keys in dicts, incorrect
    ADT usage, wrongfully using ellipsis, and much more.

    See <https://lintjl.readthedocs.org/en/stable/> for more information
    on the analysis provided.
    """
    LANGUAGES = "Julia"

    @staticmethod
    def create_arguments(filename, file, config_file):
        lintcode = ('import Lint.lintfile; lintfile("' +
                    escape(filename, '"\\') + '")')
        return '-e', lintcode
