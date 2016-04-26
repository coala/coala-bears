import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.results.Result import Result
from coalib.settings.Setting import path


@linter(executable='tslint')
class TSLintBear:
    """
    Check TypeScript code for style violations and possible semantical
    problems.

    Read more about the capabilities at
    <https://github.com/palantir/tslint#core-rules>.
    """

    LANGUAGES = "TypeScript"

    @staticmethod
    def create_arguments(filename, file, config_file,
                         tslint_config: path="", rules_dir: path=""):
        """
        :param tslint_config: Path to configuration file.
        :param rules_dir:     Rules directory
        """
        args = ('--format', 'json')
        if tslint_config:
            args += ('--config', tslint_config)
        if rules_dir:
            args += ('--rules-dir', rules_dir)
        return args + (filename,)

    def process_output(self, output, filename, file):
        output = json.loads(output) if output else []
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
