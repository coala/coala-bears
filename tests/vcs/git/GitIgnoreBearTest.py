import os
import platform
import shutil
import stat
import unittest
import unittest.mock
from queue import Queue
from tempfile import mkdtemp

from bears.vcs.git.GitIgnoreBear import GitIgnoreBear
from coalib.testing.BearTestHelper import generate_skip_decorator
from coalib.misc.Shell import run_shell_command
from coalib.settings.Section import Section


@generate_skip_decorator(GitIgnoreBear)
class GitIgnoreBearTest(unittest.TestCase):

    @staticmethod
    def run_git_command(*args, stdin=None):
        run_shell_command(' '.join(('git',) + args), stdin)

    def run_uut(self, *args, **kwargs):
        """
        Runs the unit-under-test (via `self.uut.run()`) and collects the
        messages of the yielded results as a list.

        :param args:   Positional arguments to forward to the run function.
        :param kwargs: Keyword arguments to forward to the run function.
        :return:       A list of the message strings.
        """
        return list(result.message for result in self.uut.run(*args, **kwargs))

    def assert_no_msgs(self):
        """
        Assert that there are no messages in the message queue of the bear, and
        show the messages in the failure message if it is not empty.
        """
        self.assertTrue(
            self.msg_queue.empty(),
            'Expected no messages in bear message queue, but got: ' +
            str(list(str(i) for i in self.msg_queue.queue)))

    def setUp(self):
        self.msg_queue = Queue()
        self.section = Section('')
        self.uut = GitIgnoreBear(None, self.section, self.msg_queue)

        self._old_cwd = os.getcwd()
        self.gitdir = mkdtemp()
        os.chdir(self.gitdir)
        self.run_git_command('init')
        self.run_git_command('config', 'user.email coala@coala.io')
        self.run_git_command('config', 'user.name coala')

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

    def test_check_prerequisites(self):
        _shutil_which = shutil.which
        try:
            shutil.which = lambda *args, **kwargs: None
            self.assertEqual(GitIgnoreBear.check_prerequisites(),
                             'git is not installed.')

            shutil.which = lambda *args, **kwargs: 'path/to/git'
            self.assertTrue(GitIgnoreBear.check_prerequisites())
        finally:
            shutil.which = _shutil_which

    def test_no_tracked_files(self):
        self.assertEqual(self.run_uut(), [])
        self.assert_no_msgs()

    def test_no_gitignore_file(self):
        file = open('test_file.txt', 'w')
        file.close()
        self.run_git_command('add', 'test_file.txt')

        self.assertEqual(self.run_uut(), [])
        self.assert_no_msgs()

    def test_already_tracked_file(self):
        file = open('test_file.txt', 'w')
        file.close()
        self.run_git_command('add', 'test_file.txt')

        file = open('.gitignore', 'w')
        file.write('test_file.txt')
        file.close()

        self.run_git_command('add', '.gitignore')
        self.assertEqual(self.run_uut(), [
            'File test_file.txt is being tracked which was ignored in line'
            ' number 1 in file .gitignore.'
        ])
        self.assert_no_msgs()

    def test_untracked_file(self):
        file = open('test_file.txt', 'w')
        file.close()

        file = open('.gitignore', 'w')
        file.write('test_file.txt')
        file.close()

        self.run_git_command('add', '.gitignore')
        self.assertEqual(self.run_uut(), [])
        self.assert_no_msgs()
