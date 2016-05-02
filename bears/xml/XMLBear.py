import itertools
import re

from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import path, url


def path_or_url(xml_dtd):
    """
    Coverts the setting value to url or path.

    :param xml_dtd: Setting key.
    :return:        Returns a converted setting value.
    """
    try:
        return url(xml_dtd)
    except ValueError:
        return path(xml_dtd)


@linter(executable='xmllint',
        use_stderr=True)
class XMLBear:
    """
    Checks the code with ``xmllint``.
    """
    output_regex = re.compile(r'.*:(?P<line>\d+): (?P<message>.*)\n.*\n.*')

    @staticmethod
    def create_arguments(filename, file, config_file,
                         xml_schema: path = "",
                         xml_dtd: path_or_url = ""):
        """
        :param xml_schema: ``W3C XML Schema`` file used for validation.
        :param xml_dtd:    ``Document type Definition (DTD)`` file or
                           url used for validation.
        """
        args = (filename,)
        if xml_schema:
            args += ('-schema', xml_schema)
        if xml_dtd:
            args += ('-dtdvalid', xml_dtd)
        return args

    def process_output(self, output, filename, file):
        if output[0]:
            # Return issues from stderr and stdout if stdout is not empty
            return itertools.chain(
                self.process_output_regex(
                    output[1], filename, file,
                    output_regex=self.output_regex),
                self.process_output_corrected(
                    output[0], filename, file,
                    diff_message="XML can be formatted better."))
        else:  # Return issues from stderr if stdout is empty
            return self.process_output_regex(
                output[0], filename, file,
                output_regex=self.output_regex)
