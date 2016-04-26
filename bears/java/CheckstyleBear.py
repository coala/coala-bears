import os

from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import path


DIR_PATH = os.path.dirname(os.path.abspath(__file__))

checkstyle_jar_file = os.path.join(DIR_PATH, 'checkstyle.jar')

known_checkstyles = {
    "google": os.path.join(DIR_PATH, 'google_checks.xml')}


def known_checkstyle_or_path(setting):
    if str(setting) in known_checkstyles.keys():
        return str(setting)
    else:
        return path(setting)


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

    For more information, consult
    <http://checkstyle.sourceforge.net/checks.html>.
    """

    LANGUAGES = "Java"

    def create_arguments(
            self, filename, file, config_file,
            checkstyle_configs: known_checkstyle_or_path="google"):
        """
        :param checkstyle_configs:
            A file containing configs to use in ``checkstyle``. It can also
            have the special values:

            - google - To follow Google's Java configurations. More info at
              <http://checkstyle.sourceforge.net/style_configs.html>.
        """
        checkstyle_configs = known_checkstyles.get(checkstyle_configs,
                                                   checkstyle_configs)

        return ('-jar', checkstyle_jar_file, '-c', checkstyle_configs, filename)
