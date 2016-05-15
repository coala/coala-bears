import re

from coalib.bearlib.abstractions.Lint import Lint, escape_path_argument
from coalib.bears.LocalBear import LocalBear
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


class PerlCriticBear(LocalBear, Lint):
    executable = 'perlcritic'
    output_regex = re.compile(
            r'(?P<line>\d+)\|(?P<column>\d+)\|(?P<severity>\d+)\|'
            r'(?P<origin>.*?)\|(?P<message>.*)')
    severity_map = {
        "1": RESULT_SEVERITY.MAJOR,
        "2": RESULT_SEVERITY.MAJOR,
        "3": RESULT_SEVERITY.NORMAL,
        "4": RESULT_SEVERITY.NORMAL,
        "5": RESULT_SEVERITY.INFO}
    LANGUAGES = "Perl"

    def run(self,
            filename,
            file,
            perlcritic_profile: str=""):
        '''
        Checks the code with perlcritic. This will run perlcritic over
        each of the files seperately

        :param perlcritic_profile: Location of the perlcriticrc config file.
        '''
        self.arguments = '--no-color --verbose "%l|%c|%s|%p|%m (%e)"'
        if perlcritic_profile:
            self.arguments += (" --profile "
                               + escape_path_argument(perlcritic_profile))
        self.arguments += " {filename}"
        return self.lint(filename)
