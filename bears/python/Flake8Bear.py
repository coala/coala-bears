import sys
import platform

from flake8.engine import *

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


if platform.system=='Windows':
    DEFAULT_CONFIG = os.path.expanduser(r'~\.flake8')
else:
    DEFAULT_CONFIG = os.path.join(
        os.getenv('XDG_CONFIG_HOME') or os.path.expanduser('~/.config'),
        'flake8')

class Flake8Bear(Lint, LocalBear):

    """ Checks the code according to pep8 and pyflake8 standards """

    self.gives_corrected = False
    def lint(self, filename, file):
        output_regex = re.compile(r'.*\.py:(?P<line>\d):(?P<column>\d):(?P<message>.*)')
        flake8_style = get_style_guide(
        config_file=DEFAULT_CONFIG, ignore=(), max_complexity=-1)
        report = flake8_style.check_files()
        output = report.get_file_results()
        return self.process_output(output, filename, file)

    def run(self,
            filename,
            file,
            max_line_length: int=80,
            ignore=(),
            flake8_format='',
            max_complexity=-1):
        return self.lint(filename, file)
