import shutil
import tempfile
import platform
import stat
import os
from os import path

import unittest
from queue import Queue
from coalib.settings.Section import Section
from coalib.misc.Shell import run_shell_command
from bears.general.CheckmanifestBear import CheckmanifestBear


class CheckmanifestBearTest(unittest.TestCase):

    @staticmethod
    def run_git_command(*args, stdin=None):
        run_shell_command(' '.join(('git',) + args), stdin)

    @staticmethod
    def _windows_rmtree_remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def setUp(self):
        self.queue = Queue()
        self.file_dict = {}
        self.section = Section('Checkmanifest')
        self.uut = CheckmanifestBear(self.file_dict, self.section,
                                     self.queue)
        self._old_cwd = os.getcwd()
        self.test_dir = tempfile.mkdtemp()
        with open(path.join(self.test_dir, 'setup.py'), 'w') as f:
            f.write('from setuptools import setup\n')
            f.write("setup(name='sample', py_modules=['sample'])\n")
            f.close()
        with open(path.join(self.test_dir, 'sample.py'), 'w') as f:
            f.write('# wow. such code. so amaze\n')
            f.close()

        f = open(path.join(self.test_dir, 'MANIFEST.in'), 'w')
        f.close()
        f = open(path.join(self.test_dir, 'unrelated.txt'), 'w')
        f.write('Hello from the other side')
        f.close()
        f = open(path.join(self.test_dir, 'rishu.cpp'), 'w')
        f.write('int main')
        f.close()
        os.chdir(self.test_dir)
        self.run_git_command('init')
        self.run_git_command('config', 'user.email coala@coala.io')
        self.run_git_command('config', 'user.name coala')
        self.run_git_command('add', '--all')

    def tearDown(self):
        os.chdir(self._old_cwd)
        if platform.system() == 'Windows':
            onerror = self._windows_rmtree_remove_readonly
        else:
            onerror = None
        shutil.rmtree(self.test_dir, onerror=onerror)

    def run_uut(self, *args, **kwargs):
        return list(result.message for result in self.uut.run(*args, **kwargs))

    def test_something(self):
        self.uut.file_dict = {path.join(self.test_dir, 'MANIFEST.in'):
                              ''}
        self.assertEqual(self.run_uut(ignore=['unrelated.txt', 'rishu.cpp']),
                         ['lists of files in version control and sdist match!'])  # Ignore LineLengthBear
        self.assertNotEqual(self.run_uut(), [])
