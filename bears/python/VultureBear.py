import re
from shutil import which

from coalib.bears.GlobalBear import GlobalBear
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.misc.Shell import run_shell_command
from coalib.results.Result import Result


class VultureBear(GlobalBear):
    LANGUAGES = {'Python', 'Python 3'}
    REQUIREMENTS = {PipRequirement('vulture', '0.10.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/82256'
    CAN_DETECT = {'Unused Code'}

    EXECUTABLE = 'vulture'
    OUTPUT_REGEX = re.compile(
        r'(?P<filename>.*):(?P<line>.*):\s*(?P<message>.*)')

    @classmethod
    def check_prerequisites(cls):
        return ('Vulture is missing. Make sure to install it using '
                '`pip3 install vulture`.'
                if which('vulture') is None else True)

    def run(self):
        """
        Check Python code for unused variables and functions using `vulture`.

        See <https://bitbucket.org/jendrikseipp/vulture> for more information.
        """
        stdout_output, _ = run_shell_command(
            (self.EXECUTABLE,) +
            tuple(filename for filename in self.file_dict.keys()),
            cwd=self.get_config_dir())

        for match in re.finditer(self.OUTPUT_REGEX, stdout_output):
            groups = match.groupdict()
            yield Result.from_values(origin=self,
                                     message=groups['message'],
                                     file=groups['filename'],
                                     line=int(groups['line']))
