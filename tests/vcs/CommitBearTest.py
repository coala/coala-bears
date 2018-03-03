import shutil
import unittest
import unittest.mock
from queue import Queue

from coalib.testing.BearTestHelper import generate_skip_decorator
from bears.vcs.CommitBear import _CommitBear
from bears.vcs.git.GitCommitBear import GitCommitBear
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting


class FakeCommitBear(_CommitBear):
    @classmethod
    def check_prerequisites(cls):
        return True

    def get_remotes():
        return 'https://fakeremotes.coala.io/this/is/fake/remote'

    def get_head_commit(self):
        return ('This is the fake head commit', '')


@generate_skip_decorator(_CommitBear)
class CommitBearTest(unittest.TestCase):

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
        self.uut = FakeCommitBear(None, self.section, self.msg_queue)

    def test_check_prerequisites(self):
        _shutil_which = shutil.which
        try:
            shutil.which = lambda *args, **kwargs: None
            self.assertEqual(GitCommitBear.check_prerequisites(),
                             'git is not installed.')

            shutil.which = lambda *args, **kwargs: 'path/to/git'
            self.assertTrue(GitCommitBear.check_prerequisites())
        finally:
            shutil.which = _shutil_which

    def test_get_metadata(self):
        metadata = FakeCommitBear.get_metadata()
        self.assertEqual(
            metadata.name,
            "<Merged signature of 'run', 'check_shortlog', 'check_body'"
            ", 'check_issue_reference'>")

        # Test if at least one parameter of each signature is used.
        self.assertIn('allow_empty_commit_message', metadata.optional_params)
        self.assertIn('shortlog_length', metadata.optional_params)
        self.assertIn('body_line_length', metadata.optional_params)
        self.assertIn('body_close_issue', metadata.optional_params)

    def test_pure_oneliner_message(self):
        self.assertEqual(self.run_uut(), [])
        self.assert_no_msgs()

    def test_nltk_download_disabled(self):
        # setUp has already initialised HgCommitBear.
        self.assertTrue(FakeCommitBear._nltk_data_downloaded)

        section = Section('commit')
        section.append(Setting('shortlog_imperative_check', 'False'))

        FakeCommitBear._nltk_data_downloaded = False
        FakeCommitBear(None, section, self.msg_queue)
        self.assertFalse(FakeCommitBear._nltk_data_downloaded)

        # reset
        FakeCommitBear._nltk_data_downloaded = True

    def test_nltk_download(self):
        # setUp has already initialised HgCommitBear.
        self.assertTrue(FakeCommitBear._nltk_data_downloaded)

        section = Section('commit')
        section.append(Setting('shortlog_imperative_check', 'True'))

        FakeCommitBear._nltk_data_downloaded = False
        FakeCommitBear(None, section, self.msg_queue)
        self.assertTrue(FakeCommitBear._nltk_data_downloaded)

    def test_nltk_download_default(self):
        # setUp has already initialised HgCommitBear.
        self.assertTrue(FakeCommitBear._nltk_data_downloaded)

        section = Section('commit')

        FakeCommitBear._nltk_data_downloaded = False
        FakeCommitBear(None, section, self.msg_queue)
        self.assertTrue(FakeCommitBear._nltk_data_downloaded)
