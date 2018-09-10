import os

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.PipRequirement import PipRequirement


@linter(executable='pyre',
        output_format='regex',
        normalize_column_numbers=True,
        output_regex=r'\s*(?P<filename>.+)\s*:(?P<line>\d+):(?P<column>\d+)'
                     r' \s*(?P<message>.+)',
        global_bear=True)
class PyreBear:
    """
    Checks Python files for errors using ``pyre``.
    """
    LANGUAGES = {'Python', 'Python 3'}
    REQUIREMENTS = {PipRequirement('pyre-check', '0.0.12')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'TypeError in statically typed variables'}
    SEE_MORE = 'https://pypi.org/project/pyre-check/'

    def create_arguments(self, config_file):
        files = tuple(self.file_dict.keys())
        commonpath = os.path.dirname(os.path.commonprefix(files))
        return '--source-directory', commonpath
