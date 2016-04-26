import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result


@linter(executable='coffeelint')
class CoffeeLintBear:
    """
    Check CoffeeScript code for a clean and consistent style.

    For more information about coffeelint, visit <http://www.coffeelint.org/>.
    """

    LANGUAGES = "CoffeeScript"

    severity_map = {'warn': RESULT_SEVERITY.NORMAL,
                    'error': RESULT_SEVERITY.MAJOR}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--reporter=raw', filename

    def process_output(self, output, filename, file):
        output = json.loads(output)

        assert len(output) == 1, "More than 1 file parsed, something went wrong"
        for item in tuple(output.values())[0]:
            yield Result.from_values(
                origin="{} ({})".format(self.name, item['rule']),
                message=item['message'],
                file=filename,
                line=item.get('lineNumber', None),
                end_line=item.get('lineNumberEnd', None),
                severity=self.severity_map[item['level']],
                additional_info=item.get('description',
                                         item.get('context', "")))
