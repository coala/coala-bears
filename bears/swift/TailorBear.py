import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.results.Result import Result
from coalib.settings.Setting import path


@linter(executable='tailor',
        output_format=None,
        prerequisite_check_command=('tailor', '-v'),
        prerequisite_check_fail_message='Tailor is not installed. Refer '
        'https://tailor.sh/ for installation details.')
class TailorBear:
    """
    Analyze Swift code and check for code style related
    warning messages.

    For more information on the analysis visit <https://tailor.sh/>
    """
    LANGUAGES = {'Swift'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/45666'
    CAN_DETECT = {'Formatting'}

    severity_map = {'warning': RESULT_SEVERITY.NORMAL,
                    'error': RESULT_SEVERITY.MAJOR}

    def process_output(self, output, filename, file):
        output = json.loads(output)

        for item in output['files'][0]['violations']:
            column = (item['location']['column']
                      if 'column' in item['location'].keys() else None)

            yield Result.from_values(
                origin='{} ({})'.format(self.name, item['rule']),
                message=item['message'],
                file=filename,
                line=item['location']['line'],
                column=column,
                severity=self.severity_map[item['severity']])

    @staticmethod
    def create_arguments(filename, file, config_file,
                         max_line_length: int=79,
                         max_class_length: int=0,
                         max_closure_length: int=0,
                         max_file_length: int=0,
                         max_function_length: int=0,
                         max_name_length: int=0,
                         max_struct_length: int=0,
                         min_name_length: int=1,
                         tailor_config: path=''):
        """
        Bear configuration arguments.
        Using '0' will disable the check.

        :param max_line_length:     maximum number of characters in a Line
                                    <0-999>.
        :param max_class_length:    maximum number of lines in a Class <0-999>.
        :param max_closure_length:  maximum number of lines in a Closure
                                    <0-999>.
        :param max_file_length:     maximum number of lines in a File <0-999>.
        :param max_function_length: maximum number of lines in a Function
                                    <0-999>.
        :param max_name_length:     maximum length of Identifier name <0-999>.
        :param max_struct_length:   maximum number od lines in a Struct
                                    <0-999>.
        :param min_name_length:     minimum number of characters in Identifier
                                    name <1-999>.
        :param tailor_config:       path to Tailor configuration file.
        """
        args = ('--format=json',
                '--max-line-length', str(max_line_length),
                '--max-class-length', str(max_class_length),
                '--max-closure-length', str(max_closure_length),
                '--max-file-length', str(max_file_length),
                '--max-function-length', str(max_function_length),
                '--max-name-length', str(max_name_length),
                '--max-struct-length', str(max_struct_length),
                '--min-name-length', str(min_name_length))
        if tailor_config:
            args += ('--config=' + tailor_config,)
        return args + (filename,)
