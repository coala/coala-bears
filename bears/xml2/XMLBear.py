import itertools
import re

from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.DistributionRequirement import (
    DistributionRequirement)
from coalib.settings.Setting import path, url


def path_or_url(xml_dtd):
    """
    Converts the setting value to url or path.

    :param xml_dtd: Setting key.
    :return:        Returns a converted setting value.
    """
    try:
        return url(xml_dtd)
    except ValueError:
        return path(xml_dtd)


@linter(executable='xmllint',
        use_stdout=True,
        use_stderr=True)
class XMLBear:
    """
    Checks the code with ``xmllint``.

    See http://xmlsoft.org/xmllint.html
    """
    LANGUAGES = {'XML'}
    REQUIREMENTS = {DistributionRequirement(apt_get='libxml2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax'}

    _output_regex = re.compile(r'.*:(?P<line>\d+): (?P<message>.*)\n.*\n.*')

    @staticmethod
    def create_arguments(filename, file, config_file,
                         xml_schema: path='',
                         xml_dtd: path_or_url=''):
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
                    output_regex=self._output_regex),
                self.process_output_corrected(
                    output[0], filename, file,
                    result_message='XML can be formatted better.'))
        else:
            # Return issues from stderr if stdout is empty
            return self.process_output_regex(
                output[1], filename, file,
                output_regex=self._output_regex)
