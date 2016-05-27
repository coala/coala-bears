from coalib.bearlib.abstractions.Linter import linter
from coalib.parsing.StringProcessing import escape


@linter(executable='Rscript',
        output_format='corrected',
        prerequisite_check_command=('Rscript', '-e', 'library(formatR)'),
        prerequisite_check_fail_message='Please install formatR for this bear '
                                        'to work.')
class FormatRBear:
    """
    Check and correct formatting of R Code using known formatR utility.
    """
    LANGUAGES = "R"

    @staticmethod
    def create_arguments(filename, file, config_file):
        rcode = ('library(formatR);'
                 'formatR::tidy_source(source="' +
                 escape(filename, '"\\') + '")')
        return '-e', rcode
