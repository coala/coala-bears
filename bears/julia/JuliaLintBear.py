from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class JuliaLintBear(LocalBear, Lint):
    executable = 'julia'
    arguments = '-e \'import Lint.lintfile; lintfile({filename})\''
    output_regex = r'(^.*\.jl):(?P<line>\d+) (?P<severity>.)\d+ (?P<message>.*)'
    use_stdout = True
    severity_map = {
        "E": RESULT_SEVERITY.MAJOR,
        "W": RESULT_SEVERITY.NORMAL,
        "I": RESULT_SEVERITY.INFO
    }

    def run(self, filename, file):
        '''
        Lints Julia code using ``Lint.jl``.
        https://github.com/tonyhffong/Lint.jl
        '''
        return self.lint(filename, file)
