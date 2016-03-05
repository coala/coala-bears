import re

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.misc.Shell import escape_path_argument
from coalib.settings.Setting import path


class CMakeLintBear(LocalBear, Lint):
    executable = 'cmakelint'
    output_regex = re.compile(
            r'(?P<file_name>\S+):(?P<line>[0-9]+): (?P<message>.*)')

    def run(self, filename, file, cmakelint_config: path=""):
        '''
        Checks the code with ``cmakelint``.

        :param cmakelint_config: The location of the cmakelintrc config file.
        '''
        self.arguments = ""
        if cmakelint_config:
            self.arguments += (' --config=' +
                               escape_path_argument(cmakelint_config))

        self.arguments += ' {filename}'
        return self.lint(filename)
