import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.results.Result import Result
from coalib.results.Diff import Diff
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='hlint')
class HaskellLintBear:
    """
    Check Haskell code for possible problems. This bear can propose patches for
    using alternative functions, simplifying code and removing redundancies.

    See <http://community.haskell.org/~ndm/darcs/hlint/hlint.htm> for more
    information.
    """

    LANGUAGES = "Haskell"

    severity_map = {"Error": RESULT_SEVERITY.MAJOR,
                    "Warning": RESULT_SEVERITY.NORMAL,
                    "Suggestion": RESULT_SEVERITY.INFO}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--json', filename

    def process_output(self, output, filename, file):
        output = json.loads(output)

        for issue in output:
            assert issue["startLine"] == issue["endLine"]
            diff = Diff(file)
            line_nr = issue["startLine"]
            line_to_change = file[line_nr-1]
            newline = line_to_change.replace(issue["from"], issue["to"])
            diff.change_line(line_nr, line_to_change, newline)

            yield Result.from_values(
                origin=self,
                message=issue["hint"],
                file=filename,
                severity=self.severity_map[issue["severity"]],
                line=issue["startLine"],
                diffs={filename: diff})
