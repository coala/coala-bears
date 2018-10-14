import os
import platform
import shutil
import stat
import unittest
import unittest.mock
from pathlib import Path
from queue import Queue
from tempfile import mkdtemp

from bears.vcs.git.GitCommitMetadataBear import GitCommitMetadataBear
from bears.vcs.git.GitLinearCommitBear import GitLinearCommitBear
from coalib.misc.Shell import run_shell_command
from coalib.settings.Section import Section
from coalib.testing.BearTestHelper import generate_skip_decorator
from .GitCommitBearTest import GitCommitBearTest


@generate_skip_decorator(GitLinearCommitBear)
class GitLinearCommitBearTest(unittest.TestCase):

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
        self.uut = GitLinearCommitBear(None, self.section, self.msg_queue)

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

    def test_check_git_merge_commit(self):
        Path('testfile2.txt').touch()
        run_shell_command('git add testfile2.txt')
        run_shell_command('git commit -m "Commit in master branch"')
        run_shell_command('git checkout -b new-feature1 master')
        Path('testfile3.txt').touch()
        run_shell_command('git add testfile3.txt')
        run_shell_command('git commit -m "Commit in feature branch1"')
        run_shell_command('git checkout master')
        run_shell_command('git merge --no-ff new-feature1')
        self.assertEqual(self.run_uut(),
                         ['Merge commit is not allowed. '
                          'Please perform git rebase instead. '
                          'http://www.bitsnbites.eu/a-tidy-linear-git-history/'
                          ' shows how to do rebasing.'])

    def test_check_git_merge_commit_in_coala(self):
        Path('testfile4.txt').touch()
        run_shell_command('git add testfile4.txt')
        run_shell_command('git commit -m "Commit in master branch"')
        run_shell_command('git checkout -b new-feature2 master')
        Path('testfile5.txt').touch()
        run_shell_command('git add testfile5.txt')
        run_shell_command('git commit -m "Commit in feature branch2"')
        run_shell_command('git checkout master')
        run_shell_command('git merge --no-ff new-feature2')
        self.assertEqual(
            self.run_uut(git_rebase_help_url='http://api.coala.io/en/'
                         'latest/Developers/Git_Basics.html'
                         '#rebasing'),
            ['Merge commit is not allowed. '
             'Please perform git rebase instead. '
             'http://api.coala.io/en/latest/Developers/Git_Basics.html'
             '#rebasing shows how to do rebasing.'])
