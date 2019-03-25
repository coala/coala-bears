from coalib.bearlib.abstractions.Linter import linter


@linter(executable='dos2unix',
        output_format='corrected',
        result_message='done')
class Dos2UnixBear:
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_FIX = {'Formatting'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--', filename
