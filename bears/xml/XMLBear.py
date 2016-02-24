from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class XMLBear(LocalBear, Lint):
    executable = 'xmllint'
    arguments = '{filename}'
    diff_message = "XML can be formatted better."
    gives_corrected = True

    def process_output(self, output, filename, file):
        if self.stdout_output:  # only yield Result if stdout is not empty
            return self._process_corrected(output, filename, file)

    def run(self, filename, file):
        '''
        Checks the code with `xmllint`.
        '''
        return self.lint(filename, file)
