from coalib.bearlib.abstractions.Linter import linter
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='Rscript',
        output_format='corrected',
        prerequisite_check_command=('Rscript', '-e',
                                    "\'library(formatR)\'"),
        prerequisite_check_fail_message='Please install formatR for this bear '
                                        'to work.')
class FormatRBear:
    """
    This bear checks and corrects formatting of R Code using known formatR
    utility.
    """
    LANGUAGES = "R"

    @staticmethod
    def create_arguments(filename, file, config_file):
        rcode = ("formatR::tidy_source(source=" + "\""+filename+"\")")
        args = ('-e', "library(formatR)", '-e',)
        return args + (rcode,)
