from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='pyflakes',
        use_stderr=True,
        output_format='regex',
        output_regex=r'.*:(?P<line>\d+):'
                     r'[(?P<column>\d+):|?]*(?P<severity>)\s(?P<message>.*)\n',
        severity_map={
            '': RESULT_SEVERITY.INFO
        })
class PyFlakesBear:
    """
    Checks Python files for errors using ``pyflakes``.

    See https://github.com/PyCQA/pyflakes for more info.
    """
    LANGUAGES = {'Python', 'Python 3'}
    REQUIREMENTS = {PipRequirement('pyflakes', '1.3.*')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/92503'
    CAN_DETECT = {'Syntax', 'Unused Code', 'Undefined Element'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
