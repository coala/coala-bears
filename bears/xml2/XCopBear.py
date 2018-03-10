import itertools
import re

from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from dependency_management.requirements.GemRequirement import GemRequirement


@linter(executable='xcop')
class XCopBear:
    """
    This bear can fix formatting errors in your XML, XSD, XSL, XHTML file.
    """
    LANGUAGES = {'XML', 'XSD', 'XSL', 'XHTML'}
    REQUIREMENTS = {GemRequirement('xcop')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}
    SEE_MORE = 'https://github.com/yegor256/xcop'

    _output_regex = re.compile(
        r'.*:(?P<line>\d+):.*(?P<severity>error|warning)\s?: '
        r'(?P<message>.*)\n.*\n.*')

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,

    def process_output(self, output, filename, file):
        stdout = output
        invalid_format = re.compile(r'\x1b\[31m.+?0m', re.S)
        correct_formating = filename + ' looks good\n'

        if(stdout != correct_formating):
            """Output of Xcop is colour coded in the terminal to
               identify the changes suggested by xcop.Green to indicate
               addition and red to denote subtraction.

               This introduces redundancies in the output file.
               ^[[31m denoting subtraction (i.e red colour on terminal)
               and ^[[32m denoting green.

               Thus to remove these redundancies regex is used"""

            stdout = re.sub(r'Invalid XML formatting in ' +
                            filename+'\n', '', stdout)
            stdout = re.sub(r'\\n', '', stdout)
            stdout = re.sub(invalid_format, '', stdout)
            stdout = re.sub(r'\x1b.+32m', '', stdout)
            stdout = re.sub(r'\x1b.+0m', '', stdout)
            return itertools.chain(
                self.process_output_corrected
                (stdout, filename, file,
                 diff_severity=RESULT_SEVERITY.INFO,
                 result_message='XML can be formatted better.'))
