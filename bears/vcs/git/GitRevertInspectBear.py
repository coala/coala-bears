import re

from difflib import SequenceMatcher

from bears.vcs.git.GitCommitMetadataBear import GitCommitMetadataBear
from coalib.bears.GlobalBear import GlobalBear
from coalib.misc.Shell import run_shell_command
from coalib.results.Result import Result


class GitRevertInspectBear(GlobalBear):
    LANGUAGES = {'Git'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/225921'

    BEAR_DEPS = {GitCommitMetadataBear}

    GIT_REVERT_COMMIT_RE = re.compile(
        r'Revert\s\".+\"\n\nThis\sreverts\scommit\s([0-9a-f]{40})\.')

    def _check_modified_file_similarity(self, file_path,
                                        reverted_commit_sha,
                                        minimum_similarity_ratio):
        """
        Compare the changes in file modified by the
        revert commit with the changes actually
        expected in the revert commit.

        :param file_path:                   Relative path to the modified
                                            file.
        :param reverted_commit_sha:         Commit hash of reverted commit.
        :param minimum_similarity_ratio:    Minimum similarity ratio
                                            required by files in revert
                                            commit.
        """
        def clean_inspect_revert_branch():
            run_shell_command('git checkout master')
            run_shell_command('git branch -D inspectrevertbranch')

        with open(file_path, 'r') as f:
            revert_file_content = f.read()

        create_new_branch_command = (
            'git checkout -b inspectrevertbranch HEAD^')
        run_shell_command(create_new_branch_command)

        create_expected_revert_commit = ('git revert %s --no-'
                                         'edit' %
                                         reverted_commit_sha)
        _, err = run_shell_command(create_expected_revert_commit)
        if err:
            self.warn('Cannot compare the modified files.')
            run_shell_command('git revert --abort')
            clean_inspect_revert_branch()
            return

        expected_revert_commit_sha = run_shell_command(
            'git rev-parse HEAD')[0].strip('\n')

        with open(file_path, 'r') as f:
            expected_revert_file_content = f.read()

        matcher = SequenceMatcher(
            None, revert_file_content, expected_revert_file_content)
        similarity_ratio = matcher.real_quick_ratio()
        if similarity_ratio < minimum_similarity_ratio:
            yield Result(self, 'Changes in modified file %s of '
                         'the revert commit are not exactly '
                         'revert of changes in the reverted '
                         'commit.' %
                         file_path)

        clean_inspect_revert_branch()

    def run(self, dependency_results,
            allow_git_revert_commit: bool = True,
            minimum_similarity_ratio: float = 0.8,
            **kwargs):
        """
        Inspect the HEAD commit to check if it is a
        git revert commit and return result accordingly.

        :param allow_git_revert_commit:     Whether revert commit
                                            is allowed or not.
        :param minimum_similarity_ratio:    Minimum similarity ratio
                                            required by files in revert
                                            commit.
        """
        result_string = ('Revert commit has a {} file {} '
                         'that is not in the reverted commit.')

        for result in dependency_results[GitCommitMetadataBear.name]:

            m = self.GIT_REVERT_COMMIT_RE.match(result.raw_commit_message)
            if not m:
                return

            if not allow_git_revert_commit:
                yield Result(self, 'Revert commit is not allowed.')
                return

            reverted_commit_sha = m.group(1)
            get_files_command = ('git show --pretty="" --name-status %s' %
                                 reverted_commit_sha)

            all_files = run_shell_command(get_files_command)[0]
            files_modified_by_reverted_commit = all_files.split('\n')

            reverted_commit_modified_files_list = []
            reverted_commit_added_files_list = []
            reverted_commit_deleted_files_list = []

            for line in files_modified_by_reverted_commit:
                pos = line.find('\t')
                change = line[:pos]
                if change == 'M':
                    reverted_commit_modified_files_list.append(line[pos+1:])
                elif change == 'A':
                    reverted_commit_added_files_list.append(line[pos+1:])
                elif change == 'D':
                    reverted_commit_deleted_files_list.append(line[pos+1:])

            for file_path in result.added_files:
                if file_path not in reverted_commit_deleted_files_list:
                    yield Result(self, result_string.format(
                        'added', file_path))

            for file_path in result.deleted_files:
                if file_path not in reverted_commit_added_files_list:
                    yield Result(self, result_string.format(
                        'deleted', file_path))

            for file_path in result.modified_files:
                if file_path in reverted_commit_modified_files_list:
                    yield from self._check_modified_file_similarity(
                        file_path, reverted_commit_sha,
                        minimum_similarity_ratio)

                else:
                    yield Result(self, result_string.format(
                        'modified', file_path))
