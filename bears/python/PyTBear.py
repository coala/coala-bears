import re

from coalib.bearlib.abstractions.Linter import linter
from coalib.results.Result import Result
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='pyt')
class PyTBear:
    """
    Uses pyt executable which performs security analysis
    on Python source code, utilizing the ``ast``
    module from the Python standard library.
    """
    LANGUAGES = {'Python 3'}
    REQUIREMENTS = {PipRequirement('taint-analysis', '0.11')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Security'}

    severity_map = {'High': RESULT_SEVERITY.MAJOR,
                    'Medium': RESULT_SEVERITY.NORMAL,
                    'Weak': RESULT_SEVERITY.INFO}

    def create_arguments(self, filename, file, config_file):
        args = ('-f', filename)

        return args

    def process_output(self, output, filename, file):
        # Retrieves all the variables
        # which are being tainted by user input
        regex_tainted_input = r'File: (?P<filename>.*)\n' \
                              r' > User input at line (?P<line>\d+)'

        # Retrieves all the variables which are being
        # modified by an already tainted variable
        regex_variable_tainted = r'\tFile: (?P<filename>.*)\n' \
                                 r'\t > Line (?P<line>\d+): '\
                                 r'(?P<modified_variable>.*)=(?P<modifier>.*)'

        # Retrieves all the instances where a tainted
        # variable is used to perform critical function
        regex_tainted_variable_execution = r'File: (?P<filename>.*)\n' \
                                           r' > reaches line (?P<line>\d+), '\
                                           r'trigger word "(?P<trigger>.*)":'\
                                           r' \n\t(?P<line_information>.*)'

        for tainted_input in re.finditer(regex_tainted_input, output):
            yield Result.from_values(
                origin=self,
                file=tainted_input.groupdict()['filename'],
                line=int(tainted_input.groupdict()['line']),
                severity=self.severity_map['Medium'],
                message='Input from user is being taken')

        for variable_tainted in re.finditer(regex_variable_tainted, output):
            yield Result.from_values(
                origin=self,
                file=variable_tainted.groupdict()['filename'],
                line=int(variable_tainted.groupdict()['line']),
                severity=self.severity_map['Weak'],
                message='Variable {} is being modified using {}'.format(
                         variable_tainted.groupdict()['modified_variable'],
                         variable_tainted.groupdict()['modifier']))

        for tainted_variable_execution in re.finditer(
                regex_tainted_variable_execution, output):
            yield Result.from_values(
                origin=self,
                file=tainted_variable_execution.groupdict()['filename'],
                severity=self.severity_map['High'],
                line=int(tainted_variable_execution.groupdict()['line']),
                message='Tainted variable is being executed')
