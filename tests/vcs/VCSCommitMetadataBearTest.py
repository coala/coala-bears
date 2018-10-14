import os
import platform
import shutil
import unittest
import unittest.mock
from pathlib import Path
from queue import Queue
from tempfile import mkdtemp

from bears.vcs.VCSCommitMetadataBear import (VCSCommitMetadataBear,
                                             CommitResult, COMMIT_TYPE)
from bears.vcs.git.GitCommitMetadataBear import GitCommitMetadataBear
from coalib.misc.Shell import run_shell_command
from coalib.settings.Section import Section
from coalib.testing.BearTestHelper import generate_skip_decorator


class FakeCommitBear(VCSCommitMetadataBear):
    @classmethod
    def check_prerequisites(cls):
        return True

    def get_head_commit_sha(self):
        raise RuntimeError('RuntimeError from test')


@generate_skip_decorator(VCSCommitMetadataBear)
class InvalidCommitResultTest(unittest.TestCase):

    def run_uut(self, *args, **kwargs):
        """
        Runs the unit-under-test (via `self.uut.run()`) and collects the
        messages of the yielded results as a list.

        :param args:   Positional arguments to forward to the run function.
        :param kwargs: Keyword arguments to forward to the run function.
        :return:       A list of result values that give information related
                       to head commit.
        """
        return list(result.message for result in self.uut.run(*args, **kwargs))

    def setUp(self):
        self.msg_queue = Queue()
        self.section = Section('')
        self.uut = FakeCommitBear(None, self.section, self.msg_queue)

        self._old_cwd = os.getcwd()
        self.tempdir = mkdtemp()
        os.chdir(self.tempdir)

    def test_check_prerequisites(self):
        _shutil_which = shutil.which
        try:
            shutil.which = lambda *args, **kwargs: None
            self.assertEqual(GitCommitMetadataBear.check_prerequisites(),
                             'git is not installed.')

            shutil.which = lambda *args, **kwargs: 'path/to/git'
            self.assertTrue(GitCommitMetadataBear.check_prerequisites())
        finally:
            shutil.which = _shutil_which

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
        shutil.rmtree(self.tempdir, onerror=onerror)

    def test_get_head_commit_sha(self):
        Path('testfile.txt').touch()
        run_shell_command('git add testfile.txt')
        run_shell_command('git commit -m "Add testfile"')
        self.assertEqual(self.run_uut(), [])


class CommitResultTest(unittest.TestCase):
    def setUp(self):
        self.raw_commit_message = 'raw_commit_message'
        self.commit_sha = 'commit_sha'
        self.parent_commits = ['parent_commits']
        self.modified_files = ['modified_files']
        self.added_files = ['added_files']
        self.deleted_files = ['deleted_files']

    def test_commitresult_object_repr(self):
        repr_result = repr(CommitResult(VCSCommitMetadataBear,
                                        self.raw_commit_message,
                                        self.commit_sha,
                                        self.parent_commits,
                                        COMMIT_TYPE.simple_commit,
                                        self.modified_files,
                                        self.added_files,
                                        self.deleted_files,))

        repr_regex = (
            r'<CommitResult object\(id=.+, origin=\'bearclass\', '
            r'raw_commit_message=\'.+\', '
            r'commit_sha=\'.+\', '
            r'parent_commits=\[.+\], '
            r'commit_type=<COMMIT_TYPE.simple_commit: 0>, '
            r'modified_files=\[.+\], '
            r'added_files=\[.+\], '
            r'deleted_files=\[.+\]\) at .+>'
            )
        self.assertRegex(repr_result, repr_regex)
