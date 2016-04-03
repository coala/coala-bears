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
    Lints Julia code using ``Lint.jl``.
    https://github.com/tonyhffong/Lint.jl
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        lintcode = ('import Lint.lintfile; lintfile("' +
                    escape(filename, '"\\') + '")')
        return '-e', lintcode
