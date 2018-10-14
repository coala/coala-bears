import os
import shutil

from bears.vcs.CommitBear import _CommitBear
from coala_utils.ContextManagers import change_directory
from coalib.misc.Shell import run_shell_command


class HgCommitBear(_CommitBear):
    LANGUAGES = {'Hg'}
    CAN_DETECT = {'Formatting'}

    @classmethod
    def check_prerequisites(cls):
        if shutil.which('hg') is None:
            return 'hg is not installed.'
        else:
            return True

    def get_remotes():
        remotes, _ = run_shell_command('hg paths')
        return remotes

    def get_head_commit(self):
        with change_directory(self.get_config_dir() or os.getcwd()):
            return run_shell_command('hg log -l 1 --template "{desc}"')
