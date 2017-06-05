
from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='planemo',
        output_format='regex',
        output_regex=r'..\s(?P<severity>\w*:)(?P<message>.*)',
        severity_map={'WARNING:': RESULT_SEVERITY.MAJOR,
                      'CHECK:': RESULT_SEVERITY.NORMAL,
                      'INFO:': RESULT_SEVERITY.INFO})
class PlanemoLintBear:
    """
    Checks the code with planemo lint. This will run
    planemo lint over each file separately.
    """
    LANGUAGES = {'galaxy'}
    REQUIREMENTS = {PipRequirement('planemo', '0.36'),
                    PipRequirement('lxml', '3.6.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    ASCIINEMA_URL = 'https://asciinema.org/a/0kiduzg55d59nxhm8wuwfvl3n'
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        args = ('lint',)
        return args + (filename,)
