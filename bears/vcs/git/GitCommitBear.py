import os
import shutil
import re

from bears.vcs.CommitBear import _CommitBear
from coala_utils.ContextManagers import change_directory
from coalib.misc.Shell import run_shell_command


class GitCommitBear(_CommitBear):
    LANGUAGES = {'Git'}
    ASCIINEMA_URL = 'https://asciinema.org/a/0X91Mc3z1SMW4SuRTpfXq8RMN'

    @classmethod
    def check_prerequisites(cls):
        if shutil.which('git') is None:
            return 'git is not installed.'
        else:
            return True

    def get_remotes():
        remotes, _ = run_shell_command(
            "git config --get-regex '^remote.*.url$'")
        return remotes

    def get_head_commit(self):
        with change_directory(self.get_config_dir() or os.getcwd()):
            command = self.check_github_pull_request_temporary_merge_commit()
            if command:
                return run_shell_command(command)

            return run_shell_command('git log -1 --pretty=%B')

    def check_github_pull_request_temporary_merge_commit(self):
        """
        This function creates a git command to fetch the
        unmerged parent commit shortlog from a commit generated
        by GitHub in a refs/pull/(\\d+)/merge git remote reference.
        Visit https://github.com/travis-ci/travis-ci/issues/8400
        for more details.

        :return: A git command (str) to fetch the unmerged parent
                 commit if HEAD commit is a GitHub PR temporary
                 merge commit, otherwise None"
        """
        stdout, _ = run_shell_command('git log -1 --pretty=%B')

        pos = stdout.find('\n')
        shortlog = stdout[:pos] if pos != -1 else stdout

        github_pull_request_temporary_merge_commit_regex = re.compile(
            r'^Merge ([0-9a-f]{40}) into ([0-9a-f]{40})$')
        match = re.fullmatch(
            github_pull_request_temporary_merge_commit_regex, shortlog)

        if match:
            unmerged_commit_sha = match.group(1)

            command = ('git log -n 1 --pretty=%B ' +
                       unmerged_commit_sha)

            return command
