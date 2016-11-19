from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.DistributionRequirement import (
    DistributionRequirement)


@linter(executable='verilator',
        output_format='regex',
        use_stderr=True,
        output_regex=r'\%(?:(?P<severity>Error|Warning.*?).*?):'
                     r'.+?:(?P<line>.+?): (?P<message>.+)')
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
    LANGUAGES = {'Verilog'}
    REQUIREMENTS = {DistributionRequirement(apt_get='verilator')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/45275'
    CAN_DETECT = {'Formatting', 'Code Simplification', 'Syntax', 'Unused Code'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--lint-only', filename
