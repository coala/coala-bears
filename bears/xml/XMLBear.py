import itertools

from coalib.bearlib.abstractions.Lint import Lint, escape_path_argument
from coalib.bears.LocalBear import LocalBear
from coalib.settings.Setting import path, url


def path_or_url(xml_dtd):
    '''
    Coverts the setting value to url or path.

    :param xml_dtd: Setting key.
    :return:        Returns a converted setting value.
    '''
    try:
        return url(xml_dtd)
    except ValueError:
        return path(xml_dtd)


class XMLBear(LocalBear, Lint):
    executable = 'xmllint'
    diff_message = "XML can be formatted better."
    output_regex = r'(.*\.xml):(?P<line>\d+): (?P<message>.*)\n.*\n.*'
    gives_corrected = True
    use_stderr = True
    LANGUAGES = "XML"

    def process_output(self, output, filename, file):
        if self.stdout_output:
            # Return issues from stderr and stdout if stdout is not empty
            return itertools.chain(
                self._process_issues(self.stderr_output, filename),
                self._process_corrected(self.stdout_output, filename, file))
        else:  # Return issues from stderr if stdout is empty
            return self._process_issues(self.stderr_output, filename)

    def run(self, filename, file,
            xml_schema: path="",
            xml_dtd: path_or_url=""):
        '''
        Checks the code with ``xmllint``.

        :param xml_schema: ``W3C XML Schema`` file used for validation.
        :param xml_dtd:    ``Document type Definition (DTD)`` file or
                           url used for validation.
        '''
        self.arguments = "{filename} "
        if xml_schema:
            self.arguments += " -schema " + escape_path_argument(xml_schema)
        if xml_dtd:
            self.arguments += " -dtdvalid " + xml_dtd
        return self.lint(filename, file)
