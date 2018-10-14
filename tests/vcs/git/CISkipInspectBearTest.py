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
from bears.vcs.git.CISkipInspectBear import CISkipInspectBear
from coalib.misc.Shell import run_shell_command
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.testing.BearTestHelper import generate_skip_decorator
from .GitCommitBearTest import GitCommitBearTest


@generate_skip_decorator(CISkipInspectBear)
class CISkipInspectBearTest(unittest.TestCase):

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
        self.section = Section('commit')
        self.section.append(Setting('files', '*Test.py, .coafile'))
        self.uut = CISkipInspectBear(None, self.section, self.msg_queue)

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

    def test_skipci_build_commit(self):
        Path('file1.txt').touch()
        run_shell_command('git add file1.txt')
        run_shell_command('git commit -m "Add file1"')
        self.assertEqual(
            self.run_uut(appveyor_ci=True), [])

        Path('file2.txt').touch()
        run_shell_command('git add file2.txt')
        run_shell_command('git commit -m "Add file2  [ci skip]"')
        self.assertEqual(
            self.run_uut(appveyor_ci=True), [])

        Path('file3.txt').touch()
        run_shell_command('git add file3.txt')
        run_shell_command('git commit -m "Add file3  [ci skip]"')
        self.assertEqual(
            self.run_uut(appveyor_ci=True), [])

        Path('AbcBearTest.py').touch()
        run_shell_command('git add AbcBearTest.py')
        run_shell_command(
            'git commit -m "AbcBearTest.py: Add first commit\n\n[ci skip]"')
        self.assertEqual(
            self.run_uut(appveyor_ci=True), [])

        Path('DefBearTest.py').touch()
        run_shell_command('git add DefBearTest.py')
        run_shell_command(
            'git commit -m "DefBearTest.py: Add next commit\n\n[ci skip]"')
        self.assertEqual(
            self.run_uut(),
            ['This commit modifies a file that has pattern of type '
             '"*Test.py", thus should not disable CI build.'])

        Path('DefBearTest.py').touch()
        run_shell_command('git add DefBearTest.py')
        run_shell_command(
            'git commit -m "DefBearTest.py: Add next commit [ci skip]"')
        self.assertEqual(
            self.run_uut(),
            ['This commit modifies a file that has pattern of type '
             '"*Test.py", thus should not disable CI build.'])

        Path('.coafile').touch()
        run_shell_command('git add .coafile')
        run_shell_command('git commit -m ".coafile: Add coafile [skip ci]"')
        self.assertEqual(
            self.run_uut(appveyor_ci=True),
            ['This commit modifies a file that has pattern of type '
             '".coafile", thus should not disable CI build.'])
