import itertools
import re
import logging

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)
from coalib.settings.Setting import path, url
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


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


def xml_style_valid(xml_style):
    """
    Checks if xml_style is valid.
    :param xml_style: Setting key.
    :return:          Returns the value if valid else returns none.
    """
    style = str(xml_style)
    if style not in XMLBear._styles:
        logging.warn('Unrecognised style ' + style + '. Valid xml'
                     ' styles are c14n, c14n11, exc-c14n and oldxml10.'
                     ' Running XMLBear without any xml_style argument.')
        return None
    return '--' + style


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

    _output_regex = re.compile(
        r'.*:(?P<line>\d+):.*(?P<severity>error|warning)\s?: '
        r'(?P<message>.*)\n.*\n.*')
    _diff_severity = RESULT_SEVERITY.INFO
    _styles = ('c14n', 'c14n11', 'exc-c14n', 'oldxml10')

    def create_arguments(self, filename, file, config_file,
                         xml_schema: path='',
                         xml_dtd: path_or_url='',
                         xml_style: xml_style_valid=None):
        """
        :param xml_schema: ``W3C XML Schema`` file used for validation.
        :param xml_dtd:    ``Document type Definition (DTD)`` file or
                           url used for validation.
        :param xml_style:  ``XML Style Specification`` Relevant args are
                           c14n, c14n11, exc-c14n and oldxml10.
                           Find out more about the formats at
                           https://www.w3.org/TR/#tr_XML_Canonicalization
        """
        args = (filename,)
        if xml_schema:
            args += ('-schema', xml_schema)
        if xml_dtd:
            args += ('-dtdvalid', xml_dtd)
        if xml_style:
            args += (xml_style,)
            self._diff_severity = RESULT_SEVERITY.MAJOR

        return args

    def process_output(self, output, filename, file):
        stdout, stderr = output
        if stdout:
            # Return issues from stderr and stdout if stdout is not empty
            return itertools.chain(
                self.process_output_regex(
                    stderr, filename, file,
                    output_regex=self._output_regex),
                self.process_output_corrected(
                    stdout, filename, file,
                    diff_severity=self._diff_severity,
                    result_message='XML can be formatted better.'))
        else:
            # Return issues from stderr if stdout is empty
            return self.process_output_regex(
                stderr, filename, file,
                output_regex=self._output_regex)
