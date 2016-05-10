from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='verilator',
        output_format='regex',
        use_stderr=True,
        output_regex=r'\%(?:(?P<severity>Error|Warning.*?).*?):'
        r'.+?:(?P<line>.+?): '
        r'(?P<message>.+)',
        severity_map={'Error': RESULT_SEVERITY.MAJOR,
                      'Warning': RESULT_SEVERITY.NORMAL})
class VerilogLintBear:
    """
    Analyze Verilog code using ``verilator`` and checks for all lint
    related and code style related warning messages. It supports the
    synthesis subset of Verilog, plus initial statements, proper
    blocking/non-blocking assignments, functions, tasks.

    It also warns about unused code when a specified signal is never sinked,
    and unoptimized code due to some construct, with which the
    optimization of the specified signal or block is disabled.

    This is done using the ``--lint-only`` command. For more information visit
    <http://www.veripool.org/projects/verilator/wiki/Manual-verilator>.
    """
    LANGUAGES = "Verilog"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--lint-only', filename
