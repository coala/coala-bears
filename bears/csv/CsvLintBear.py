from coalib.bearlib.abstractions.Linter import linter


@linter(executable='csvlint',
        output_format='regex',
        output_regex=r'\d\. (?P<message>.+)\. Row:'
                     r' (?P<row>\d+)\. (?P<information>.+)',
        result_message='This ``csv`` file is invalid.')
class CsvLintBear:
    """
    Verifies using ``csvlint`` if ``.csv`` files are valid csv or not.
    """

    LANGUAGES = {"csv"}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
