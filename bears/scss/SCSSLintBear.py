from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='scss-lint', output_format="regex",
        output_regex=r'.+:(?P<line>\d+)\s+(\[(?P<severity>.)\])\s*'
                     r'(?P<message>.*)',
        severity_map={'I': RESULT_SEVERITY.INFO,
                      'W': RESULT_SEVERITY.NORMAL,
                      'E': RESULT_SEVERITY.MAJOR})
class SCSSLintBear:
    """
    Checks the code with ``scss-lint`` on each file separately.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
