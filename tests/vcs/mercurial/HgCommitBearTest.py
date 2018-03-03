import os
import platform
import shutil
import stat
import unittest
import unittest.mock
from queue import Queue
from tempfile import mkdtemp

from coalib.testing.BearTestHelper import generate_skip_decorator
from bears.vcs.mercurial.HgCommitBear import HgCommitBear
from coalib.misc.Shell import run_shell_command
from coalib.settings.Section import Section


@generate_skip_decorator(HgCommitBear)
class HgCommitBearTest(unittest.TestCase):

    test_file = 'test_file.txt'

    @staticmethod
    def run_hg_command(*args, stdin=None):
        run_shell_command(' '.join(('hg',) + args), stdin)

    @staticmethod
    def hg_commit(msg):
        if msg == '':
            msg = ' '
        with open(HgCommitBearTest.test_file, 'w') as f:
            f.write(msg)
        HgCommitBearTest.run_hg_command('commit -l ',
                                        HgCommitBearTest.test_file)

    def changeHgConfig(self, newConfig):
        with open(self.hgdir + '/.hg/hgrc', 'w') as f:
            f.write(newConfig)

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
        self.uut = HgCommitBear(None, self.section, self.msg_queue)

        self._old_cwd = os.getcwd()
        self.hgdir = mkdtemp()
        os.chdir(self.hgdir)
        self.run_hg_command('init')
        run_shell_command('touch ' + HgCommitBearTest.test_file)
        self.run_hg_command('add', HgCommitBearTest.test_file)
        new_config_file = ('[ui]\n'
                           'username = user.email <coala@coala.io>')
        self.changeHgConfig(new_config_file)
        self.run_hg_command('commit -m "testInit Commit"')

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
        shutil.rmtree(self.hgdir, onerror=onerror)

    def test_check_prerequisites(self):
        _shutil_which = shutil.which
        try:
            shutil.which = lambda *args, **kwargs: None
            self.assertEqual(HgCommitBear.check_prerequisites(),
                             'hg is not installed.')

            shutil.which = lambda *args, **kwargs: 'path/to/hg'
            self.assertTrue(HgCommitBear.check_prerequisites())
        finally:
            shutil.which = _shutil_which

    def test_hg_failure(self):
        # The only case where hg log gives error is in case its not a repo
        # so do a log on non-existent repo to perform failure check
        run_shell_command('mv .hg .hgback')
        self.assertEqual(self.run_uut(), [])
        run_shell_command('mv .hgback .hg')

        hg_error = self.msg_queue.get().message
        self.assertEqual(hg_error[:3], 'hg:')

        self.assert_no_msgs()

    def test_empty_message(self):
        self.hg_commit('')

        self.assertEqual(self.run_uut(),
                         ['HEAD commit has no message.'])
        self.assert_no_msgs()

        self.assertEqual(self.run_uut(allow_empty_commit_message=True),
                         [])
        self.assert_no_msgs()

    def test_shortlog_checks_length(self):
        self.hg_commit('Commit messages that nearly exceed default limit..')

        self.assertEqual(self.run_uut(), [])
        self.assert_no_msgs()

        self.assertEqual(self.run_uut(shortlog_length=17),
                         ['Shortlog of the HEAD commit contains 50 '
                          'character(s). This is 33 character(s) longer than '
                          'the limit (50 > 17).'])
        self.assert_no_msgs()

        self.hg_commit('Add a very long shortlog for a bad project history.')
        self.assertEqual(self.run_uut(),
                         ['Shortlog of the HEAD commit contains 51 '
                          'character(s). This is 1 character(s) longer than '
                          'the limit (51 > 50).'])
        self.assert_no_msgs()

    def test_shortlog_checks_shortlog_trailing_period(self):
        self.hg_commit('Shortlog with dot.')
        self.assertEqual(self.run_uut(shortlog_trailing_period=True), [])
        self.assertEqual(self.run_uut(shortlog_trailing_period=False),
                         ['Shortlog of HEAD commit contains a period at end.'])
        self.assertEqual(self.run_uut(shortlog_trailing_period=None), [])

        self.hg_commit('Shortlog without dot')
        self.assertEqual(
            self.run_uut(shortlog_trailing_period=True),
            ['Shortlog of HEAD commit contains no period at end.'])
        self.assertEqual(self.run_uut(shortlog_trailing_period=False), [])
        self.assertEqual(self.run_uut(shortlog_trailing_period=None), [])

    def test_shortlog_wip_check(self):
        self.hg_commit('[wip] Shortlog')
        self.assertEqual(self.run_uut(shortlog_wip_check=False), [])
        self.assertEqual(self.run_uut(shortlog_wip_check=True),
                         ['This commit seems to be marked as work in progress '
                          'and should not be used in production. Treat '
                          'carefully.'])
        self.assertEqual(self.run_uut(shortlog_wip_check=None), [])
        self.hg_commit('Shortlog as usual')
        self.assertEqual(self.run_uut(shortlog_wip_check=True), [])

    def test_shortlog_checks_imperative(self):
        self.hg_commit('tag: Add shortlog in imperative')
        self.assertNotIn("Shortlog of HEAD commit isn't in imperative "
                         "mood! Bad words are 'added'",
                         self.run_uut())
        self.hg_commit('Added invalid shortlog')
        self.assertIn("Shortlog of HEAD commit isn't in imperative "
                      "mood! Bad words are 'Added'",
                      self.run_uut())
        self.hg_commit('Adding another invalid shortlog')
        self.assertIn("Shortlog of HEAD commit isn't in imperative "
                      "mood! Bad words are 'Adding'",
                      self.run_uut())
        self.hg_commit('Added another invalid shortlog')
        self.assertNotIn("Shortlog of HEAD commit isn't in imperative "
                         "mood! Bad words are 'Added'",
                         self.run_uut(shortlog_imperative_check=False))

    def test_shortlog_checks_regex(self):
        pattern = '.*?: .*[^.]'

        self.hg_commit('tag: message')
        self.assertEqual(self.run_uut(shortlog_regex=pattern), [])

        self.hg_commit('tag: message invalid.')
        self.assertEqual(
            self.run_uut(shortlog_regex=pattern),
            ['Shortlog of HEAD commit does not match given regex: {regex}'
             .format(regex=pattern)])

        self.hg_commit('SuCkS cOmPleTely')
        self.assertEqual(
            self.run_uut(shortlog_regex=pattern),
            ['Shortlog of HEAD commit does not match given regex: {regex}'
             .format(regex=pattern)])
        # Check for full-matching.
        pattern = 'abcdefg'

        self.hg_commit('abcdefg')
        self.assertEqual(self.run_uut(shortlog_regex=pattern), [])

        self.hg_commit('abcdefgNO MATCH')
        self.assertEqual(
            self.run_uut(shortlog_regex=pattern),
            ['Shortlog of HEAD commit does not match given regex: {regex}'
             .format(regex=pattern)])

    def test_body_checks(self):
        self.hg_commit(
            'Commits message with a body\n\n'
            'nearly exceeding the default length of a body, but not quite. '
            'haaaaaands')

        self.assertEqual(self.run_uut(), [])
        self.assert_no_msgs()

        self.hg_commit('Shortlog only')

        self.assertEqual(self.run_uut(), [])
        self.assert_no_msgs()

        # Force a body.
        self.hg_commit('Shortlog only ...')
        self.assertEqual(self.run_uut(force_body=True),
                         ['No commit message body at HEAD.'])
        self.assert_no_msgs()

        # Miss a newline between shortlog and body.
        self.hg_commit('Shortlog\nOops, body too early')
        self.assertEqual(self.run_uut(),
                         ['No newline found between shortlog and body at '
                          'HEAD commit. Please add one.'])
        self.assert_no_msgs()

        # And now too long lines.
        self.hg_commit('Shortlog\n\n'
                       'This line is ok.\n'
                       'This line is by far too long (in this case).\n'
                       'This one too, blablablablablablablablabla.')
        self.assertEqual(self.run_uut(body_line_length=41),
                         ['Body of HEAD commit contains too long lines. '
                          'Commit body lines should not exceed 41 '
                          'characters.'])
        self.assert_no_msgs()

        # Allow long lines with ignore regex
        self.hg_commit('Shortlog\n\n'
                       'This line is ok.\n'
                       'This line is by far too long (in this case).')
        self.assertEqual(self.run_uut(body_line_length=41,
                                      ignore_length_regex=('^.*too long',)),
                         [])
        self.assertTrue(self.msg_queue.empty())

        # body_regex, not fully matched
        self.hg_commit('Shortlog\n\n'
                       'First line, blablablablablabla.\n'
                       'Another line, blablablablablabla.\n'
                       'Fix 1112')
        self.assertEqual(self.run_uut(
                             body_regex=r'Fix\s+[1-9][0-9]*\s*'),
                         ['No match found in commit message for the regular '
                          r'expression provided: Fix\s+[1-9][0-9]*\s*'])
        self.assert_no_msgs()

        # Matching with regexp, fully matched
        self.hg_commit('Shortlog\n\n'
                       'TICKER\n'
                       'CLOSE 2017')
        self.assertEqual(self.run_uut(
                             body_regex=r'TICKER\s*CLOSE\s+[1-9][0-9]*'), [])
        self.assert_no_msgs()

    def test_check_issue_reference(self):
        # Commit with no remotes configured
        self.hg_commit('Shortlog\n\n'
                       'First line, blablablablablabla.\n'
                       'Another line, blablablablablabla.\n')
        self.assertEqual(self.run_uut(body_close_issue=True), [])

        # Commit with a compatible remote (bitbucket https)
        new_config_file = ('[paths]\n'
                           'test=https://user@bitbucket.org/user/hgrepo')
        self.changeHgConfig(new_config_file)

        self.hg_commit('Shortlog\n\n'
                       'First line, blablablablablabla.\n'
                       'Another line, blablablablablabla.\n')
        self.assertEqual(self.run_uut(body_close_issue=True,
                                      body_enforce_issue_reference=True),
                         ['Body of HEAD commit does not contain any '
                          'issue reference.'])

        self.hg_commit('Shortlog\n\n'
                       'First line, blablablablablabla.\n'
                       'Another line, blablablablablabla.\n'
                       'Closes #01112')
        self.assertEqual(self.run_uut(body_close_issue=True,
                                      body_enforce_issue_reference=True),
                         ['Invalid issue number: #01112'])

        # Adding incompatible remote for testing
        new_config_file = ('[paths]\n'
                           'test=http://hg.sv.gnu.org/hgweb/project')
        self.changeHgConfig(new_config_file)

        # Unsupported Host - savannah
        self.hg_commit('Shortlog\n\n'
                       'First line, blablablablablabla.\n'
                       'Another line, blablablablablabla.\n'
                       'Closes #1112')
        self.assertEqual(self.run_uut(
                         body_close_issue=True,
                         body_close_issue_full_url=True), [])

        # SSH BitBucket Remote (compatible remote)
        new_config_file = ('[paths]\n'
                           'test=ssh://hg@bitbucket.org/user/repo')
        self.changeHgConfig(new_config_file)

        self.hg_commit('Shortlog\n\n'
                       'First line, blablablablablabla.\n'
                       'Another line, blablablablablabla.\n')
        self.assertEqual(self.run_uut(body_close_issue=True,
                                      body_enforce_issue_reference=True),
                         ['Body of HEAD commit does not contain any '
                          'issue reference.'])

        self.hg_commit('Shortlog\n\n'
                       'First line, blablablablablabla.\n'
                       'Another line, blablablablablabla.\n'
                       'Closes #01112')
        self.assertEqual(self.run_uut(body_close_issue=True,
                                      body_enforce_issue_reference=True),
                         ['Invalid issue number: #01112'])

        # No keywords and no issues
        self.hg_commit('Shortlog\n\n'
                       'This line is ok.\n'
                       'This line is by far too long (in this case).\n'
                       'This one too, blablablablablablablablabla.')
        self.assertEqual(self.run_uut(
                              body_close_issue=True,
                              body_close_issue_full_url=True,
                              body_close_issue_on_last_line=True),
                         ['Host bitbucket does not support full issue '
                          'reference.'])
        self.assert_no_msgs()

        # No keywords, no issues, no body
        self.hg_commit('Shortlog only')
        self.assertEqual(self.run_uut(body_close_issue=True,
                                      body_close_issue_on_last_line=True), [])
        self.assert_no_msgs()

        # Has keyword but no valid issue URL
        self.hg_commit('Shortlog\n\n'
                       'First line, blablablablablabla.\n'
                       'Another line, blablablablablabla.\n'
                       'Fix https://user@bitbucket.org/user/mercurialrepo')
        self.assertEqual(self.run_uut(
                             body_close_issue=True,
                             body_close_issue_full_url=True),
                         ['Host bitbucket does not support full issue '
                          'reference.'])
        self.assert_no_msgs()

        # Bitbucket host with short issue tag
        self.hg_commit('Shortlog\n\n'
                       'First line, blablablablablabla.\n'
                       'Another line, blablablablablabla.\n'
                       'Fix #1112, #1115 and #123')
        self.assertEqual(self.run_uut(body_close_issue=True), [])

        # Bitbucket host with invalid short issue tag
        self.hg_commit('Shortlog\n\n'
                       'First line, blablablablablabla.\n'
                       'Another line, blablablablablabla.\n'
                       'Fix #01112 and #111')
        self.assertEqual(self.run_uut(body_close_issue=True,),
                         ['Invalid issue number: #01112'])
        self.assert_no_msgs()

        # Bitbucket host with no full issue reference
        self.hg_commit('Shortlog\n\n'
                       'First line, blablablablablabla.\n'
                       'Another line, blablablablablabla.\n'
                       'Fix #1112')
        self.assertEqual(self.run_uut(
                             body_close_issue=True,
                             body_close_issue_full_url=True),
                         ['Host bitbucket does not support full issue '
                          'reference.'])
        self.assert_no_msgs()

        # Invalid characters in issue number
        self.hg_commit('Shortlog\n\n'
                       'First line, blablablablablabla.\n'
                       'Another line, blablablablablabla.\n'
                       'Fix #1112-3')
        self.assertEqual(self.run_uut(
                             body_close_issue=True),
                         ['Invalid issue reference: #1112-3'])
        self.assert_no_msgs()

        # One of the short references is broken
        self.hg_commit('Shortlog\n\n'
                       'First line, blablablablablabla.\n'
                       'Another line, blablablablablabla.\n'
                       'Resolve #11 and closes #notnum')
        self.assertEqual(self.run_uut(body_close_issue=True),
                         ['Invalid issue reference: #notnum'])
        self.assert_no_msgs()

        # Incorrect close issue other repo pattern
        self.hg_commit('Shortlog\n\n'
                       'First line, blablablablablabla.\n'
                       'Another line, blablablablablabla.\n'
                       'Fix #11 and close bitbucket#32')
        self.assertEqual(self.run_uut(body_close_issue=True),
                         ['Invalid issue reference: bitbucket#32'])
        self.assert_no_msgs()
