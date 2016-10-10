import re
from shutil import which

from coalib.bears.GlobalBear import GlobalBear
from coalib.bears.requirements.PipRequirement import PipRequirement
from coalib.misc.Shell import run_shell_command


class VultureBear(GlobalBear):
    LANGUAGES = {"Python", "Python 3"}
    REQUIREMENTS = {PipRequirement('happiness', '0.10.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/82256'
    CAN_DETECT = {'Unused Code'}

    executable = "vulture"
    arguments = (executable,)
    output_regex = re.compile(
        r'(?P<filename>.*):(?P<line>.*):\s*(?P<message>.*)')

    @classmethod
    def check_prerequisites(cls):  # pragma: no cover
        if which("bash") is None:
            return "bash is not installed."
        if which("vulture") is None:
            return ("Vulture is missing. Make sure to install it using "
                    "``pip3 install happiness``.")
        else:
            return True

    def run(self, filename):
    """
    Checks Python code for unused variables and functions using ``vulture``.

    See <https://bitbucket.org/jendrikseipp/vulture> for more information.
    """
    self.arguments = self.executable + ' {filename}'
    stdout_output, _ = run_shell_command(self.arguments)
