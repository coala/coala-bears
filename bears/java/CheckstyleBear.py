from os.path import abspath, dirname, join

from coalib.bearlib.abstractions.Linter import linter


checkstyle_jar_file = join(dirname(abspath(__file__)), 'checkstyle.jar')
google_checks = join(dirname(abspath(__file__)), 'google_checks.xml')


@linter(executable='java',
        output_format='regex',
        output_regex=r'\[(?P<severity>WARN|INFO)\] *.+:'
                     r'(?P<line>\d+)(?::(?P<column>\d+))?: *'
                     r'(?P<message>.*?) *\[(?P<origin>[a-zA-Z]+?)\]',
        prerequisite_check_command=('java', '-jar', checkstyle_jar_file, '-v'),
        prerequisite_check_fail_message='jar file ' + checkstyle_jar_file +
                                        ' not found.')
class CheckstyleBear:
    """
    Checks the code with ``checkstyle`` using the Google codestyle
    specification.
    """

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '-jar', checkstyle_jar_file, '-c', google_checks, filename
