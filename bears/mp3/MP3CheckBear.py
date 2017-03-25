from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


@linter(executable='mp3check')
class MP3CheckBear(LocalBear):
    """
    Report possible security weaknesses for MP3 files.
    For more information,
    consult <https://code.google.com/archive/p/mp3check/>.
    """
    LANGUAGES = {'MP3'}
    REQUIREMENTS = {DistributionRequirement(apt_get='mp3check')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    USE_RAW_FILES = True

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '-ase', filename

    def process_output(self, output, filename, file):
        lines = output.split('\n')
        lines = (i for i in lines)
        for msg in lines:
            yield Result.from_values(origin=self,
                                     message=msg,
                                     file=filename,
                                     severity=RESULT_SEVERITY.MAJOR)
