from coalib.bearlib.abstractions.Linter import linter
from coalib.bearlib.spacing.SpacingHelper import SpacingHelper


@linter(executable='Rscript',
        output_format='corrected',
        prerequisite_check_command=('Rscript', '-e', "library(formatR)"),
        prerequisite_check_fail_message='Please install formatR for this bear '
                                        'to work.')
class FormatRBear:
    """
    This bear checks and corrects formatting of R Code using known formatR
    utility.
    """
    LANGUAGES = "R"

    @staticmethod
    def create_arguments(filename, file, config_file,
                         comment: str="TRUE",
                         blank: str="TRUE",
                         brace: str="FALSE",
                         arrow: str="FALSE",
                         tab_width: int=SpacingHelper.DEFAULT_TAB_WIDTH,
                         max_line_length: int=80,
                         output: str="TRUE",
                         output_file: str=""):
        """
        :param comment:         Use to determine whether comments are
                                kept or not
        :param blank:           Use to determine whether blank lines
                                are kept or not
        :param brace:           Whether to put the left brace
        :param arrow:           Whether to replace the assign operator = with <-
        :param tab_width:       Number of space for indentation
        :param max_line_length: Maximum number of characters for a line.
        :param output:          Use to output to the console or a file
        :output_file:           The file to which the resulting is written
        """
        rcode = ("formatR::tidy_source("
                 "source=\"{filename}\","
                 "comment={comment},"
                 "blank={blank},"
                 "arrow={arrow},"
                 "width.cutoff={max_line_length},"
                 "brace.newline={brace},"
                 "indent={tab_width},"
                 "output={output},"
                 "file=\"{output_file}\""
                 ")".format(filename=filename, comment=comment, blank=blank,
                            arrow=arrow, brace=brace, output=output,
                            max_line_length=max_line_length,
                            tab_width=tab_width, output_file=output_file))
        args = ('-e', "library(formatR)", '-e',)
        return args + (rcode,)
