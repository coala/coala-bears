import os
import platform
import shutil
import stat
import sys
import unittest
import unittest.mock
from pathlib import Path
from queue import Queue
from tempfile import mkdtemp

from bears.vcs.git.GitCommitMetadataBear import GitCommitMetadataBear
from bears.vcs.git.GitRevertInspectBear import GitRevertInspectBear
from coalib.misc.Shell import run_shell_command, ShellCommandResult
from coalib.settings.Section import Section
from coalib.testing.BearTestHelper import generate_skip_decorator
from .GitCommitBearTest import GitCommitBearTest


@generate_skip_decorator(GitRevertInspectBear)
class GitRevertInspectBearTest(unittest.TestCase):

    def run_uut(self, *args, **kwargs):
        """
        Runs the unit-under-test (via `self.uut.run()`) and collects the
        messages of the yielded results as a list.

        :param args:   Positional arguments to forward to the run function.
        :param kwargs: Keyword arguments to forward to the run function.
        :return:       A list of the message strings.
        """
        dep_bear = GitCommitMetadataBear(None, self.section, Queue())
        deps_results = dict(GitCommitMetadataBear=list(dep_bear.run()))
        return list(result.message for result in self.uut.run(
            deps_results, *args, **kwargs))

    def setUp(self):
        self.msg_queue = Queue()
        self.section = Section('')
        self.uut = GitRevertInspectBear(None, self.section, self.msg_queue)

        self._old_cwd = os.getcwd()
        self.gitdir = mkdtemp()
        os.chdir(self.gitdir)
        GitCommitBearTest.run_git_command('init')
        GitCommitBearTest.run_git_command(
            'config', 'user.email coala@coala.io')
        GitCommitBearTest.run_git_command('config', 'user.name coala')

    @staticmethod
    def _windows_rmtree_remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def tearDown(self):
        os.chdir(self._old_cwd)
        if platform.system() == 'Windows':
            onerror = self._windows_rmtree_remove_readonly
        else:
            onerror = None
        shutil.rmtree(self.gitdir, onerror=onerror)

    def test_check_simple_git_commit(self):
        Path('testfile1.txt').touch()
        run_shell_command('git add testfile1.txt')
        run_shell_command('git commit -m "Add testfile1"')
        self.assertEqual(self.run_uut(), [])

    def test_check_revert_commit_not_allowed(self):
        Path('testfile1.txt').touch()
        run_shell_command('git add testfile1.txt')
        run_shell_command('git commit -m "Add testfile1"')
        run_shell_command('git revert HEAD --no-edit')
        self.assertEqual(self.run_uut(
            allow_git_revert_commit=False),
            ['Revert commit is not allowed.'])

    def test_check_git_revert_commit_with_extra_added_file(self):
        Path('testfile1.txt').touch()
        with open('testfile1.txt', 'w') as f:
            f.write('Modify text')
        Path('testfile2.txt').touch()
        with open('testfile2.txt', 'w') as f:
            f.write('Modify text')
        run_shell_command('git add testfile1.txt')
        run_shell_command('git add testfile2.txt')
        run_shell_command('git commit -m "reverted commit"')

        run_shell_command('git revert HEAD --no-edit')
        Path('testfile3.txt').touch()
        run_shell_command('git add testfile3.txt')
        run_shell_command('git commit --amend --allow-empty --no-edit')

        self.assertEqual(self.run_uut(),
                         ['Revert commit has a added file testfile3.txt that '
                          'is not in the reverted commit.'])

    def test_check_git_revert_commit_with_extra_deleted_file(self):
        Path('testfile1.txt').touch()
        with open('testfile1.txt', 'w') as f:
            f.write('Some text')

        Path('testfile2.txt').touch()
        with open('testfile2.txt', 'w') as f:
            f.write('Some more text')

        run_shell_command('git add testfile1.txt')
        run_shell_command('git add testfile2.txt')
        run_shell_command('git commit -m "intial commit"')

        run_shell_command('git rm testfile1.txt')
        run_shell_command('git commit -m "delete file"')

        run_shell_command('git revert HEAD --no-edit')
        run_shell_command('git rm testfile2.txt')
        run_shell_command('git commit --amend --allow-empty --no-edit')

        self.assertEqual(self.run_uut(),
                         ['Revert commit has a deleted file testfile2.txt '
                          'that is not in the reverted commit.'])

    def test_check_git_revert_commit_with_extra_modified_file(self):
        Path('testfile1.txt').touch()
        with open('testfile1.txt', 'w') as f:
            f.write('Some text\n')

        Path('testfile2.txt').touch()
        with open('testfile2.txt', 'w') as f:
            f.write('Some more text\n')

        run_shell_command('git add testfile1.txt')
        run_shell_command('git add testfile2.txt')
        run_shell_command('git commit -m "intial commit"')

        with open('testfile1.txt', 'a') as f:
            f.write('Changed text\n')
        run_shell_command('git add testfile1.txt')
        run_shell_command('git commit -m "modified file"')

        run_shell_command('git revert HEAD --no-edit')
        with open('testfile2.txt', 'w') as f:
            f.write('Some more changed text\n')
        run_shell_command('git add testfile2.txt')
        run_shell_command('git commit --amend --allow-empty --no-edit')

        self.assertEqual(self.run_uut(),
                         ['Revert commit has a modified file testfile2.txt '
                          'that is not in the reverted commit.'])

        Path('testfile3.txt').touch()
        with open('testfile3.txt', 'w') as f:
            f.write('Some text\n')
        run_shell_command('git add testfile3.txt')
        run_shell_command('git commit -m "Initial commit"')

        with open('testfile3.txt', 'a') as f:
            f.write('Changed text\n')
        run_shell_command('git add testfile3.txt')
        run_shell_command('git commit -m "modify testfile3"')

        run_shell_command('git revert HEAD --no-edit')
        self.assertEqual(
            self.run_uut(minimum_similarity_ratio=0.7), [])

    def test_check_file_similarity_with_invalid_revert_commit(self):
        Path('testfile5.txt').touch()
        with open('testfile5.txt', 'w') as f:
            f.write('Some text\n')
        run_shell_command('git add testfile5.txt')
        run_shell_command('git commit -m "Initial commit"')

        with open('testfile5.txt', 'a') as f:
            f.write('Changed text\n')
        run_shell_command('git add testfile5.txt')
        run_shell_command('git commit -m "modify testfile5"')

        run_shell_command('git revert HEAD --no-edit')
        with open('testfile5.txt', 'a') as f:
            f.write('Some text\nSome more text\n')
        run_shell_command('git add testfile5.txt')
        run_shell_command('git commit --amend --allow-empty --no-edit')
        with open('testfile5.txt', 'a') as f:
            f.write('Even more text.\n')
        run_shell_command('git add testfile5.txt')
        run_shell_command('git commit --amend --allow-empty --no-edit')
        with open('testfile5.txt', 'a') as f:
            f.write('Last line\n')
        run_shell_command('git add testfile5.txt')
        run_shell_command('git commit --amend --allow-empty --no-edit')
        self.assertEqual(self.run_uut(),
                         ['Changes in modified file testfile5.txt of the '
                          'revert commit are not exactly revert of changes '
                          'in the reverted commit.'])

    def test_check_file_similarity_with_correct_revert_commit(self):
        Path('testfile6.txt').touch()
        with open('testfile6.txt', 'w') as f:
            f.write('Some other text\n')
        run_shell_command('git add testfile6.txt')
        run_shell_command('git commit -m "Initial commit"')

        with open('testfile6.txt', 'w') as f:
            f.write('Changed text\n')
        run_shell_command('git add testfile6.txt')
        run_shell_command('git commit -m "modify testfile6"')

        run_shell_command('git revert HEAD --no-edit')
        with open('testfile6.txt', 'w') as f:
            f.write('Some more text\n')
        run_shell_command('git add testfile6.txt')
        run_shell_command('git commit --amend --allow-empty --no-edit')
        self.assertEqual(self.run_uut(), [])

    @unittest.mock.patch('bears.vcs.git.GitRevertInspectBear.run_shell_command')
    def test_check_modified_file_similarity_error(self, mock_run_shell_command):
        mock_run_shell_command.side_effect = [
            ShellCommandResult(0, 'M\ttestfile7.txt', sys.stderr),
            ShellCommandResult(0, None, sys.stderr),
            ShellCommandResult(0, ('', 'errors'), sys.stderr),
            ShellCommandResult(0, None, sys.stderr),
            ShellCommandResult(0, None, sys.stderr),
            ShellCommandResult(0, None, sys.stderr)
        ]

        Path('testfile7.txt').touch()
        with open('testfile7.txt', 'w') as f:
            f.write('Some other text\n')
        run_shell_command('git add testfile7.txt')
        run_shell_command('git commit -m "Initial commit"')

        with open('testfile7.txt', 'w') as f:
            f.write('Changed text\n')
        run_shell_command('git add testfile7.txt')
        run_shell_command('git commit -m "modify testfile6"')

        run_shell_command('git revert HEAD --no-edit')
        with open('testfile7.txt', 'w') as f:
            f.write('Some more text\n')
        run_shell_command('git add testfile7.txt')
        run_shell_command('git commit --amend --allow-empty --no-edit')

        assert self.run_uut() == []
        mock_run_shell_command.assert_has_calls(
            [unittest.mock.call('git revert --abort')])
