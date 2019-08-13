import unittest
from unittest.mock import patch
from coala_utils.ContextManagers import retrieve_stdout
from coalib.results.Result import Result
from bears.vcs.actions.EditCommitMessageAction import EditCommitMessageAction


class EditCommitMessageActionTest(unittest.TestCase):

    def setUp(self):
        self.uut = EditCommitMessageAction()
        self.result = Result('origin', 'message')

    def test_is_applicable(self):
        self.assertTrue(self.uut.is_applicable(self.result, {}, {}))

    def test_apply(self):
        with retrieve_stdout() as stdout:
            patcher = ('bears.vcs.actions.EditCommitMessageAction.'
                       'subprocess.check_call')
            with patch(patcher):
                ret = self.uut.apply(self.result, {}, {'file': 'diff'})
                self.assertEqual(ret, {'file': 'diff'})
                self.assertEqual(stdout.getvalue(), '')
