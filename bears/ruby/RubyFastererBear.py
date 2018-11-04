from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GemRequirement import GemRequirement


@linter(executable='fasterer',
        output_format='regex',
        output_regex=r'(?P<message>.*\.).*:\s(?P<line>\d+)')
class RubyFastererBear:
    """
    The ``RubyFastererBear`` will suggest some speed improvements which you
    can check in details at the <https://github.com/JuanitoFatas/fast-ruby>.

    It uses ``fasterer``. See <https://www.rubydoc.info/gems/fasterer/0.4.1>
    for more info.
    """

    LANGUAGES = {'Ruby'}
    REQUIREMENTS = {GemRequirement('fasterer', '0.4.1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    ASCIINEMA_URL = 'https://asciinema.org/a/210076'
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Complexity'}
    SEE_MORE = 'https://github.com/DamirSvrtan/fasterer'

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
