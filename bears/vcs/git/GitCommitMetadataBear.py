import os
import shutil

from bears.vcs.VCSCommitMetadataBear import VCSCommitMetadataBear, COMMIT_TYPE
from coala_utils.ContextManagers import change_directory
from coalib.misc.Shell import run_shell_command


class GitCommitMetadataBear(VCSCommitMetadataBear):
    LANGUAGES = {'Git'}

    @classmethod
    def check_prerequisites(cls):
        if shutil.which('git') is None:
            return 'git is not installed.'
        else:
            return True

    def get_head_commit_sha(self):
        with change_directory(self.get_config_dir() or os.getcwd()):
            (stdout, stderr) = run_shell_command('git rev-parse HEAD')

            if stderr:
                vcs_name = list(self.LANGUAGES)[0].lower()+':'
                self.err(vcs_name, repr(stderr))
                raise RuntimeError('The directory is not a git repository.')

            head_commit_sha = stdout.strip('\n')
            return head_commit_sha

    def analyze_commit(self, head_commit_sha):
        commit_type = COMMIT_TYPE.simple_commit

        command = 'git log -1 --pretty=%B ' + head_commit_sha
        head_commit = run_shell_command(command)[0]

        get_parent_commits = 'git log --pretty=%P -n 1 ' + head_commit_sha
        all_parent_commits = run_shell_command(get_parent_commits)[0]
        parent_commits_list = all_parent_commits.split(' ')

        if len(parent_commits_list) >= 2:
            commit_type |= COMMIT_TYPE.merge_commit

        get_all_committed_files = ('git show --pretty="" --name-status ' +
                                   head_commit_sha)
        all_committed_files = run_shell_command(get_all_committed_files)[0]
        all_committed_files = all_committed_files.split('\n')

        modified_files_list = []
        added_files_list = []
        deleted_files_list = []

        for line in all_committed_files:
            pos = line.find('\t')
            change = line[:pos]
            if change == 'M':
                modified_files_list.append(line[pos+1:])
            elif change == 'A':
                added_files_list.append(line[pos+1:])
            elif change == 'D':
                deleted_files_list.append(line[pos+1:])

        yield (head_commit, head_commit_sha, parent_commits_list,
               commit_type, modified_files_list, added_files_list,
               deleted_files_list)
