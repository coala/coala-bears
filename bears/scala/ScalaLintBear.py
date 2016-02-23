from os.path import abspath, dirname, join
import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.misc.Shell import escape_path_argument
from bears.CheckPrerequisites import check_linter_prerequisites_builder


class ScalaLintBear(LocalBear, Lint):
    executable = 'java'
    current_file_dir = dirname(abspath(__file__))
    jar = join(current_file_dir, 'scalastyle.jar')
    scalastyle_config_file = join(current_file_dir, 'scalastyle_config.xml')

    output_regex = re.compile(
        r'(?P<severity>warning)\s(file=)(?P<filename>.+)\s(message=)'
        r'(?P<message>.+)(line=)(?P<line>\d+)(\s(column=)(?P<column>\d+))*'
    )

    severity_map = {
        "warning": RESULT_SEVERITY.NORMAL
    }

    prerequisites_args_list = [
        "java", "-jar", jar, "-c",
        scalastyle_config_file, ".", "-q", "true"
    ]
    prerequisites_fail_msg = "jar file {} is invalid and cannot be used".format(
        jar)

    check_linter_prerequisites = check_linter_prerequisites_builder(
                                     executable,
                                     prerequisites_args_list,
                                     prerequisites_fail_msg
                                     )
    check_prerequisites = classmethod(check_linter_prerequisites)

    def run(self,
            filename,
            file,
            scalalint_config: str=""):
        '''
        Checks the code with `scalastyle` on each file separately.

        :param scalalint_config: Path to a custom configuration file.
        '''
        self.arguments = ' -jar ' + self.jar
        self.arguments += ' {filename}'
        scala_config_file = self.scalastyle_config_file
        if scalalint_config:
            scala_config_file = scalalint_config
        self.arguments += (' --config ' +
                           escape_path_argument(scala_config_file))
        return self.lint(filename)
