from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='perlcritic',
        output_format='regex',
        output_regex=r'(?P<line>\d+)\|(?P<column>\d+)\|(?P<severity>\d+)\|'
                     r'(?P<origin>.*?)\|(?P<message>.*)',
        severity_map={"1": RESULT_SEVERITY.MAJOR,
                      "2": RESULT_SEVERITY.MAJOR,
                      "3": RESULT_SEVERITY.NORMAL,
                      "4": RESULT_SEVERITY.NORMAL,
                      "5": RESULT_SEVERITY.INFO})
class PerlCriticBear:
    """
    Checks the code with perlcritic. This will run perlcritic over each of the
    files separately.
    """
    LANGUAGES = "Perl"

    @staticmethod
    def create_arguments(filename, file, config_file,
                         perlcritic_profile: str=""):
        """
        :param perlcritic_profile: Location of the perlcriticrc config file.
        """
        args = ('--no-color', '--verbose', '%l|%c|%s|%p|%m (%e)')
        if perlcritic_profile:
            args += ('--profile', perlcritic_profile)
        return args + (filename,)
