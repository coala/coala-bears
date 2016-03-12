from coalib.bearlib.abstractions.Lint import Lint
from coalib.bears.LocalBear import LocalBear
from coalib.misc.Shell import escape_path_argument
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

    def process_output(self, output, filename, file):
        if self.stdout_output:  # only yield Result if stdout is not empty
            return self._process_corrected(self.stdout_output, filename, file)
        if self.stderr_output:  # pragma: no cover
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
