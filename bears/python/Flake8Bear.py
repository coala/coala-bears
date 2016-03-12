import sys
import os

from flake8.engine import get_style_guide

from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear

if sys.platform.startswith('win'):
    DEFAULT_CONFIG = os.path.expanduser(r'~\.flake8')
else:
    DEFAULT_CONFIG = os.path.join(
        os.getenv('XDG_CONFIG_HOME') or os.path.expanduser('~/.config'),
        'flake8'
    )


class Flake8Bear(Lint, LocalBear):

    """ Checks the code according to pep8 and pyflake8 standards """

    def lint(self, filename, file):
        self.gives_corrected = False

        flake8_style = get_style_guide(config_file=DEFAULT_CONFIG)
        options = flake8_style.options

        if options.install_hook:
            from flake8.hooks import install_hook
            install_hook()

        report = flake8_style.check_files()
        output = report.print_statistics()

        return self.process_output(list(output), filename, file)

    def run(self,
            filename,
            file,
            max_line_length: int=80,
            ignore=(),
            flake8_format='',
            max_complexity=-1):

        return self.lint(filename, file)
