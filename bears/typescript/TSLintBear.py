import json

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.misc.Shell import escape_path_argument
from coalib.results.Result import Result
from coalib.settings.Setting import path


class TSLintBear(LocalBear, Lint):
    executable = 'tslint'

    def process_output(self, output, filename, file):
        output = json.loads("".join(output)) if output else []
        for issue in output:
            yield Result.from_values(
                origin="{} ({})".format(self.__class__.__name__,
                                        issue['ruleName']),
                message=issue["failure"],
                file=issue["name"],
                line=int(issue["startPosition"]["line"]) + 1,
                end_line=int(issue["endPosition"]["line"]) + 1,
                column=int(issue["startPosition"]["character"]) + 1,
                end_column=int(issue["endPosition"]["character"]) + 1)

    def run(self,
            filename,
            file,
            tslint_config: path="",
            rules_dir: path=""):
        '''
        Checks the code with ``tslint`` on each file separately.

        :param tslint_config: Path to configuration file.
        :param rules_dir:     Rules directory
        '''
        self.arguments = "--format json"
        if tslint_config:
            self.arguments += (" --config " +
                               escape_path_argument(tslint_config))
        if rules_dir:
            self.arguments += (" --rules-dir " +
                               escape_path_argument(rules_dir))
        self.arguments += " {filename}"
        return self.lint(filename, file)
