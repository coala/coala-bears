import appdirs
import os
from shutil import copyfileobj
from urllib.request import urlopen

from bears import VERSION
from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import path


DIR_PATH = os.path.dirname(os.path.abspath(__file__))

checkstyle_jar_file = os.path.join(DIR_PATH, 'checkstyle.jar')

known_checkstyles = {
    "google": "https://raw.githubusercontent.com/checkstyle/checkstyle/master/src/main/resources/google_checks.xml",
    "sun": 'https://raw.githubusercontent.com/checkstyle/checkstyle/master/src/main/resources/sun_checks.xml',
    "android-check-easy": "https://raw.githubusercontent.com/noveogroup/android-check/master/android-check-plugin/src/main/resources/checkstyle/checkstyle-easy.xml",
    "android-check-hard": "https://raw.githubusercontent.com/noveogroup/android-check/master/android-check-plugin/src/main/resources/checkstyle/checkstyle-hard.xml",
    "geosoft": "http://geosoft.no/development/geosoft_checks.xml"}


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

            - google - Google's Java style. More info at
              <http://checkstyle.sourceforge.net/style_configs.html>.
            - sun - Sun's Java style. These are the same
              as the default Eclipse checks. More info at
              <http://checkstyle.sourceforge.net/style_configs.html>.
            - android-check-easy - The easy Android configs provided by the
              android-check eclipse plugin. More info at
              <https://github.com/noveogroup/android-check>.
            - android-check-hard - The hard Android confis provided by the
              android-check eclipse plugin. More info at
              <https://github.com/noveogroup/android-check>.
            - geosoft - The Java style followed by GeoSoft. More info at
              <http://geosoft.no/development/javastyle.html>
        """
        checkstyle_configs = self.known_configs(checkstyle_configs)

        return ('-jar', checkstyle_jar_file, '-c', checkstyle_configs, filename)

    def known_configs(self, key):
        url = known_checkstyles.get(key, None)
        if url is None:  # If not known, it must be custom path
            return key

        filename = os.path.join(self.data_dir, key + "_style.xml")
        if os.path.exists(filename):
            return filename

        self.info("Downloading checkstyle configs for {key} from {url}"
                  .format(key=key, url=url))
        with urlopen(url) as response, open(filename, 'wb') as out_file:
            copyfileobj(response, out_file)
        return filename

    @property
    def data_dir(self):
        _data_dir = os.path.abspath(os.path.join(
            appdirs.user_data_dir('coala-bears', version=VERSION),
            self.name))

        if not os.path.isdir(_data_dir):  # pragma: no cover
            os.makedirs(_data_dir)
        return _data_dir
