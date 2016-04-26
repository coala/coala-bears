from os.path import abspath, dirname, join

from coalib.settings.Setting import path
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
    Check Java code for possible style, semantic and design issues.

    By default the Google Java Style coding conventions are used.

    For more information, consult
    <http://checkstyle.sourceforge.net/checks.html>.
    """

    LANGUAGES = "Java"

    @staticmethod
    def create_arguments(filename, file, config_file,
                         checkstyle_config: path=google_checks):
        """
        :param checkstyle_config:
            The checkstyle configuration file to use.
        """
        return '-jar', checkstyle_jar_file, '-c', checkstyle_config, filename
