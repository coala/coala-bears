import unittest
import os
import platform
import shutil
from tempfile import mkdtemp, mkstemp
from unittest.mock import Mock

from coalib.results.Result import Result
from bears.vcs.actions.AddNewlineAction import AddNewlineAction
from coala_utils.ContextManagers import retrieve_stdout
from coalib.misc.Shell import run_shell_command


class AddNewlineActionTest(unittest.TestCase):

    @staticmethod
    def run_git_command(*args, stdin=None):
        return run_shell_command(' '.join(('git',) + args), stdin)

    def setUp(self):
        self.shortlog = 'file.py: Add something'
        self.body = ('Added something, wrote some things\n'
                     'Wrote tests\n'
                     '\n'
                     'Fixes #issue')
        self.uut = AddNewlineAction()
        self.result = Result('origin', 'message')

        # Creating a temporary git repository and
        # adding a commit to test
        self._old_cwd = os.getcwd()
        self.gitdir = mkdtemp()
        os.chdir(self.gitdir)
        self.gitfile = mkstemp(dir=self.gitdir)
        self.run_git_command('init')
        self.run_git_command('config', 'user.email coala@coala.io')
        self.run_git_command('config', 'user.name coala')
        self.msg = self.shortlog + '\n' + self.body
        self.run_git_command('add .')
        self.run_git_command('commit',
                             '--file=-',
                             stdin=self.msg)

    def tearDown(self):
        # Deleting the temporary repository
        os.chdir(self._old_cwd)
        if platform.system() == 'Windows':
            onerror = self._windows_rmtree_remove_readonly
        else:
            onerror = None
        shutil.rmtree(self.gitdir, onerror=onerror)

    def test_is_applicable_apply(self):
        # Applicable because there is no newline between shortlog and body
        self.assertTrue(self.uut.is_applicable(self.result, {}, {}))

        with retrieve_stdout() as stdout:
            self.uut.apply(self.result, {}, {})
            new_message, _ = run_shell_command('git log -1 --pretty=%B')
            new_message = new_message.rstrip('\n')
            self.assertEqual(new_message,
                             self.shortlog + '\n\n' + self.body)
            self.assertEqual(stdout.getvalue(), '')

        # Not applicable after action is applied
        self.assertFalse(self.uut.is_applicable(self.result, {}, {}))

        # Undoing the amend done by applying the action
        self.run_git_command('commit',
                             '--amend',
                             '--file=-',
                             stdin=self.msg)

    def test_is_applicable_edited_message(self):
        # Applicable because there is no newline between shortlog and body
        self.assertTrue(self.uut.is_applicable(self.result, {}, {}))

        # Mocking EditCommitMessageAction to test cases where user first
        # changes commit message by appying EditCommitMessageAction, then
        # checking the applicability of AddNewlineAction
        EditCommitMessageAction = Mock()
        edited_msg1 = ('This is new commit message\n'
                       'Still no new line')
        edited_msg2 = ('This is lastest commit message\n'
                       '\n'
                       'Finally a new line!!')

        EditCommitMessageAction.apply.side_effect = self.run_git_command(
            'commit', '--amend', '--file=-', stdin=edited_msg1)
        EditCommitMessageAction.apply()
        self.assertTrue(self.uut.is_applicable(self.result, {}, {}))

        EditCommitMessageAction.apply.side_effect = self.run_git_command(
            'commit', '--amend', '--file=-', stdin=edited_msg2)
        EditCommitMessageAction.apply()
        self.assertFalse(self.uut.is_applicable(self.result, {}, {}))
