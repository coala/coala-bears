from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear


class XMLBear(LocalBear, Lint):
    executable = 'xmllint'
    arguments = '{filename}'
    diff_message = "XML can be formatted better."
    output_regex = r'(.*\.xml):(?P<line>\d+): (?P<message>.*)\n.*\n.*'
    gives_corrected = True

    def process_output(self, output, filename, file):
        if self.stdout_output:  # only yield Result if stdout is not empty
            return self._process_corrected(self.stdout_output, filename, file)
        if self.stderr_output:  # pragma: no cover
            return self._process_issues(self.stderr_output, filename)

    def run(self, filename, file):
        '''
        Checks the code with `xmllint`.
        '''
        return self.lint(filename, file)
