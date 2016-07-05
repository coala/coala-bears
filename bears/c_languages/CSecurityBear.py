from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Setting import typed_list


@linter(executable="flawfinder", output_format="regex",
        output_regex=r'.+:(?P<line>\d+):(?P<column>\d+):\s*'
                     r'\[(?P<severity>\d)\]\s*'
                     r'\((?P<origin>.+)\) (?P<message>.+)',
        severity_map={"5": RESULT_SEVERITY.MAJOR,
                      "4": RESULT_SEVERITY.NORMAL, "3": RESULT_SEVERITY.NORMAL,
                      "2": RESULT_SEVERITY.INFO, "1": RESULT_SEVERITY.INFO})
class CSecurityBear:
    """
    Report possible security weaknesses for C/C++.

    For more information, consult <http://www.dwheeler.com/flawfinder/>.
    """

    LANGUAGES = "C", "C++"

    @staticmethod
    def create_arguments(filename, file, config_file):
        return "--columns", "--dataonly", "--quiet", "--singleline", filename
