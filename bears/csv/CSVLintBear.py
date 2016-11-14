import re

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GemRequirement import GemRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='csvlint')
class CSVLintBear:
    """
    Verifies using ``csvlint`` if ``.csv`` files are valid CSV or not.
    """

    LANGUAGES = {'CSV'}
    REQUIREMENTS = {GemRequirement('csvlint')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}
    ASCIINEMA_URL = 'https://asciinema.org/a/8fmp2pny34kpqw7t1eoy7phhc'

    regex = re.compile(r'\n\d+\.\s(?P<origin>(?P<severity>\w+))\.\s'
                       r'(Row:\s(?P<line>[0-9]+)\.\s)?(?P<message>.*)?')

    severity_map = {
        'wrong_content_type': RESULT_SEVERITY.MAJOR,
        'ragged_rows': RESULT_SEVERITY.MAJOR,
        'blank_rows': RESULT_SEVERITY.MAJOR,
        'invalid_encoding': RESULT_SEVERITY.MAJOR,
        'not_found': RESULT_SEVERITY.MAJOR,
        'stray_quote': RESULT_SEVERITY.MAJOR,
        'unclosed_quote': RESULT_SEVERITY.MAJOR,
        'whitespace': RESULT_SEVERITY.MAJOR,
        'line_breaks': RESULT_SEVERITY.MAJOR,
        'no_encoding': RESULT_SEVERITY.NORMAL,
        'encoding': RESULT_SEVERITY.NORMAL,
        'no_content_type': RESULT_SEVERITY.NORMAL,
        'excel': RESULT_SEVERITY.NORMAL,
        'check_options': RESULT_SEVERITY.NORMAL,
        'inconsistent_values': RESULT_SEVERITY.NORMAL,
        'empty_column_name': RESULT_SEVERITY.NORMAL,
        'duplicate_column_name': RESULT_SEVERITY.NORMAL,
        'title_row': RESULT_SEVERITY.NORMAL,
        'nonrfc_line_breaks': RESULT_SEVERITY.INFO,
        'assumed_header': RESULT_SEVERITY.INFO}

    message_dict = {
        'wrong_content_type': 'Content type is not text/csv.',
        'ragged_rows': 'Row has a different number of columns. (than the first'
                        ' row in the file)',
        'blank_rows': 'Completely empty row, e.g. blank line or a line where'
                       ' all column values are empty.',
        'invalid_encoding': 'Encoding error when parsing row, e.g. because of'
                             ' invalid characters.',
        'not_found': 'HTTP 404 error when retrieving the data.',
        'stray_quotd': 'Missing or stray quote.',
        'unclosed_quotd': 'Unclosed quoted field.',
        'whitespacd': 'A quoted column has leading or trailing whitespace.',
        'line_breakd': 'Line breaks were inconsistent or incorrectly'
                         ' specified.',
        'no_encodind': 'The Content-Type header returned in the HTTP request'
                         ' does not have a charset parameter.',
        'encoding': 'The character set is not UTF-8.',
        'no_content_type': 'File is being served without a Content-Type'
                           ' header.',
        'excel': 'No Content-Type header and the file extension is .xls.',
        'check_optiond': 'CSV file appears to contain only a single column.',
        'inconsistent_valued': 'Inconsistent values in the same column.'
                               ' Reported if <90% of values seem to have same'
                               ' data type. (either numeric or alphanumeric'
                               ' including punctuation)',
        'empty_column_name': 'A column in the CSV header has an empty name.',
        'duplicate_column_name': 'A column in the CSV header has a duplicate'
                                 ' name.',
        'title_rod': 'There appears to be a title field in the first row of'
                      ' the CSV.',
        'nonrfc_line_breakd': 'Uses non-CRLF line breaks, so does not conform'
                              ' to RFC4180.',
        'assumed_headed': 'The validator has assumed that a header is present.'
    }

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,

    @classmethod
    def process_output(self, output, filename, file, result_message=None):
        for match in re.finditer(self.regex, str(output)):
            groups = match.groupdict()
            result_message = ' ' + groups['message'] if groups[
                'line'] is None else ''
            yield self._convert_output_regex_match_to_result(
                self,
                match, filename, severity_map=self.severity_map,
                result_message=self.message_dict[groups['origin']] +
                               result_message)
