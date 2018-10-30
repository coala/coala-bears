from coalib.bearlib.abstractions.Linter import linter


@linter(executable='gixy',
        output_format='regex',
        result_message='done')
class GixyBear:
    @staticmethod
    def create_arguments(filename, file, config_file):
        return '--', filename
