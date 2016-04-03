from coalib.bearlib.abstractions.Linter import linter


@linter(executable='Rscript',
        prerequisite_check_command=('Rscript', '-e', '"library(formatR)"'),
        prerequisite_check_fail_message='Please install formatR for this bear '
                                        'to work.')
class FormatRBear:
    """
    This bear checks and corrects formatting of R Code using known formatR
    utility.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ('-e', 'library(formatR)', '-e',
                'formatR::tidy_source(' + filename + ')')

    def process_output(self, output, filename, file):
        output = output.splitlines(True)
        output = "".join(output[:-1] + [output[-1].strip() + "\n"])
        return self.process_corrected_output_format(
            output, filename, file,
            diff_message='Formatting can be improved.')
