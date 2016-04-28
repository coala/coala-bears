import os
import platform
import shutil
import stat
import unittest
import unittest.mock
from queue import Queue
from tempfile import mkdtemp

from tests.BearTestHelper import generate_skip_decorator
from bears.vcs.git.GitCommitBear import GitCommitBear
from coalib.misc.Shell import run_shell_command
from coalib.settings.ConfigurationGathering import get_config_directory
from coalib.settings.Section import Section
from coalib.settings.Setting import Setting
from coalib.parsing.StringProcessing import escape


@generate_skip_decorator(GitCommitBear)
class GitCommitBearTest(unittest.TestCase):

    @staticmethod
    def run_git_command(*args, stdin=None):
        run_shell_command(" ".join(("git",) + args), stdin)

    @staticmethod
    def git_commit(msg):
        # Use stdin mode from git, since -m on Windows cmd does not support
        # multiline messages.
        GitCommitBearTest.run_git_command("commit",
                                          "--allow-empty",
                                          "--allow-empty-message",
                                          "--file=-",
                                          stdin=msg)

    def run_uut(self, *args, **kwargs):
        """
        Runs the unit-under-test (via `self.uut.run()`) and collects the
        messages of the yielded results as a list.

        :param args:   Positional arguments to forward to the run function.
        :param kwargs: Keyword arguments to forward to the run function.
        :return:       A list of the message strings.
        """
        return list(result.message for result in self.uut.run(*args, **kwargs))

    def setUp(self):
        self.msg_queue = Queue()
        self.section = Section("")
        self.uut = GitCommitBear(None, self.section, self.msg_queue)

        self._old_cwd = os.getcwd()
        self.gitdir = mkdtemp()
        os.chdir(self.gitdir)
        self.run_git_command("init")
        self.run_git_command("config", "user.email coala@coala-analyzer.io")
        self.run_git_command("config", "user.name coala")

    @staticmethod
    def _windows_rmtree_remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def tearDown(self):
        os.chdir(self._old_cwd)
        if platform.system() == "Windows":
            onerror = self._windows_rmtree_remove_readonly
        else:
            onerror = None
        shutil.rmtree(self.gitdir, onerror=onerror)

    def test_check_prerequisites(self):
        _shutil_which = shutil.which
        try:
            shutil.which = lambda *args, **kwargs: None
            self.assertEqual(GitCommitBear.check_prerequisites(),
                             "git is not installed.")

            shutil.which = lambda *args, **kwargs: "path/to/git"
            self.assertTrue(GitCommitBear.check_prerequisites())
        finally:
            shutil.which = _shutil_which

    def test_get_metadata(self):
        metadata = GitCommitBear.get_metadata()
        self.assertEqual(
            metadata.name,
            "<Merged signature of 'run', 'check_shortlog', 'check_body'>")

        # Test if at least one parameter of each signature is used.
        self.assertIn("allow_empty_commit_message", metadata.optional_params)
        self.assertIn("shortlog_length", metadata.optional_params)
        self.assertIn("body_line_length", metadata.optional_params)

    def test_git_failure(self):
        # In this case use a reference to a non-existing commit, so just try
        # to log all commits on a newly created repository.
        self.assertEqual(self.run_uut(), [])

        git_error = self.msg_queue.get().message
        self.assertEqual(git_error[:4], "git:")

        self.assertTrue(self.msg_queue.empty())

    def test_empty_message(self):
        self.git_commit("")

        self.assertEqual(self.run_uut(),
                         ["HEAD commit has no message."])
        self.assertTrue(self.msg_queue.empty())

        self.assertEqual(self.run_uut(allow_empty_commit_message=True),
                         [])
        self.assertTrue(self.msg_queue.empty())

    @unittest.mock.patch("bears.vcs.git.GitCommitBear.run_shell_command",
                         return_value=("one-liner-message\n", ""))
    def test_pure_oneliner_message(self, patch):
        self.assertEqual(self.run_uut(), [])
        self.assertTrue(self.msg_queue.empty())

    def test_shortlog_checks_length(self):
        self.git_commit("Commit messages that nearly exceed default limit..")

        self.assertEqual(self.run_uut(), [])
        self.assertTrue(self.msg_queue.empty())

        self.assertEqual(self.run_uut(shortlog_length=17),
                         ["Shortlog of HEAD commit is 33 character(s) "
                          "longer than the limit (50 > 17)."])
        self.assertTrue(self.msg_queue.empty())

        self.git_commit("Add a very long shortlog for a bad project history.")
        self.assertEqual(self.run_uut(),
                         ["Shortlog of HEAD commit is 1 character(s) longer "
                          "than the limit (51 > 50)."])
        self.assertTrue(self.msg_queue.empty())

    def test_shortlog_checks_shortlog_trailing_period(self):
        self.git_commit("Shortlog with dot.")
        self.assertEqual(self.run_uut(shortlog_trailing_period=True), [])
        self.assertEqual(self.run_uut(shortlog_trailing_period=False),
                         ["Shortlog of HEAD commit contains a period at end."])
        self.assertEqual(self.run_uut(shortlog_trailing_period=None), [])

        self.git_commit("Shortlog without dot")
        self.assertEqual(
            self.run_uut(shortlog_trailing_period=True),
            ["Shortlog of HEAD commit contains no period at end."])
        self.assertEqual(self.run_uut(shortlog_trailing_period=False), [])
        self.assertEqual(self.run_uut(shortlog_trailing_period=None), [])

    def test_shortlog_wip_check(self):
        self.git_commit("[wip] Shortlog")
        self.assertEqual(self.run_uut(shortlog_wip_check=False), [])
        self.assertEqual(self.run_uut(shortlog_wip_check=True),
                         ["This commit seems to be marked as work in progress "
                          "and should not be used in production. Treat "
                          "carefully."])
        self.assertEqual(self.run_uut(shortlog_wip_check=None), [])
        self.git_commit("Shortlog as usual")
        self.assertEqual(self.run_uut(shortlog_wip_check=True), [])

    def test_shortlog_checks_imperative(self):
        self.git_commit("tag: Add shortlog in imperative")
        self.assertNotIn("Shortlog of HEAD commit isn't imperative mood, "
                         "bad words are 'Add'",
                         self.run_uut())
        self.git_commit("Added invalid shortlog")
        self.assertIn("Shortlog of HEAD commit isn't imperative mood, "
                      "bad words are 'Added'",
                      self.run_uut())
        self.git_commit("Adding another invalid shortlog")
        self.assertIn("Shortlog of HEAD commit isn't imperative mood, "
                      "bad words are 'Adding'",
                      self.run_uut())
        self.git_commit("Added another invalid shortlog")
        self.assertNotIn("Shortlog of HEAD commit isn't imperative mood, "
                         "bad words are 'Added'",
                         self.run_uut(shortlog_imperative_check=False))

    def test_shortlog_checks_regex(self):
        pattern = ".*?: .*[^.]"

        self.git_commit("tag: message")
        self.assertEqual(self.run_uut(shortlog_regex=pattern), [])

        self.git_commit("tag: message invalid.")
        self.assertEqual(
            self.run_uut(shortlog_regex=pattern),
            ["Shortlog of HEAD commit does not match given regex."])

        self.git_commit("SuCkS cOmPleTely")
        self.assertEqual(
            self.run_uut(shortlog_regex=pattern),
            ["Shortlog of HEAD commit does not match given regex."])

        # Check for full-matching.
        pattern = "abcdefg"

        self.git_commit("abcdefg")
        self.assertEqual(self.run_uut(shortlog_regex=pattern), [])

        self.git_commit("abcdefgNO MATCH")
        self.assertEqual(
            self.run_uut(shortlog_regex=pattern),
            ["Shortlog of HEAD commit does not match given regex."])

    def test_body_checks(self):
        self.git_commit(
            "Commits message with a body\n\n"
            "nearly exceeding the default length of a body, but not quite. "
            "haaaaaands")

        self.assertEqual(self.run_uut(), [])
        self.assertTrue(self.msg_queue.empty())

        self.git_commit("Shortlog only")

        self.assertEqual(self.run_uut(), [])
        self.assertTrue(self.msg_queue.empty())

        # Force a body.
        self.git_commit("Shortlog only ...")
        self.assertEqual(self.run_uut(force_body=True),
                         ["No commit message body at HEAD."])
        self.assertTrue(self.msg_queue.empty())

        # Miss a newline between shortlog and body.
        self.git_commit("Shortlog\nOops, body too early")
        self.assertEqual(self.run_uut(),
                         ["No newline between shortlog and body at HEAD."])
        self.assertTrue(self.msg_queue.empty())

        # And now too long lines.
        self.git_commit("Shortlog\n\n"
                        "This line is ok.\n"
                        "This line is by far too long (in this case).\n"
                        "This one too, blablablablablablablablabla.")
        self.assertEqual(self.run_uut(body_line_length=41),
                         ["Body of HEAD commit contains too long lines."])
        self.assertTrue(self.msg_queue.empty())

    def test_different_path(self):
        no_git_dir = mkdtemp()
        self.git_commit("Add a very long shortlog for a bad project history.")
        os.chdir(no_git_dir)
        # When section doesn't have a project_dir
        self.assertEqual(self.run_uut(), [])
        git_error = self.msg_queue.get().message
        self.assertEqual(git_error[:4], "git:")
        # when section does have a project_dir
        self.section.append(Setting("project_dir", escape(self.gitdir, '\\')))
        self.assertEqual(self.run_uut(),
                         ["Shortlog of HEAD commit is 1 character(s) longer "
                          "than the limit (51 > 50)."])
        self.assertEqual(get_config_directory(self.section),
                         self.gitdir)
        os.chdir(self.gitdir)
        os.rmdir(no_git_dir)
