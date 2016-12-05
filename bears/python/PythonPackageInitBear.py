import os

from coalib.results.Result import Result
from coalib.bears.GlobalBear import GlobalBear


class PythonPackageInitBear(GlobalBear):
    """
    Looks for missing __init__.py files in directories containing python files.
    """

    LANGUAGES = {'Python', 'Python 3', 'Python 2'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    def run(self):
        dirs = {os.path.split(filename)[0]
                for filename in self.file_dict.keys()
                if filename.endswith('.py')}

        missing_inits = {directory for directory in dirs
                         if not os.path.join(directory, '__init__.py')
                         in self.file_dict}

        for missing_init_dir in missing_inits:
            yield Result(self,
                         'Directory "{}" does not contain __init__.py file'
                         .format(os.path.relpath(missing_init_dir,
                                                 self.get_config_dir())))
