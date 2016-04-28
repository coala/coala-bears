from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class FormatRBear(Lint, LocalBear):
    executable = "Rscript"
    arguments = ("-e 'library(formatR)' "
                 "-e 'formatR::tidy_source(\"{filename}\")'")
    prerequisite_command = ['Rscript', '-e', "'library(formatR)'"]
    prerequisite_fail_msg = "Please install formatR for this bear to work."
    diff_message = "Formatting can be improved."
    gives_corrected = True
    LANGUAGES = "R"

    def process_output(self, output, filename, file):
        output = output[:-1] + (output[-1].strip()+"\n",)
        return Lint.process_output(self, output, filename, file)

    def run(self, filename, file):
        '''
        This bear checks and corrects formatting of R Code using
        known formatR utility.
        '''
        return self.lint(filename, file)
