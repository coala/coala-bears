import re
import shutil
import os

from coalib.bears.GlobalBear import GlobalBear
from coalib.misc.ContextManagers import change_directory
from coalib.misc.Shell import run_shell_command
from coalib.results.Result import Result


class GitCommitBear(GlobalBear):

    @classmethod
    def check_prerequisites(cls):
        if shutil.which("git") is None:
            return "git is not installed."
        else:
            return True

    def run(self,
            shortlog_length: int=50,
            body_line_length: int=73,
            force_body: bool=False,
            allow_empty_commit_message: bool=False,
            shortlog_regex: str="",
            shortlog_trailing_period: bool=None):
        """
        Checks the current git commit message at HEAD.

        This bear ensures that the shortlog and body do not exceed a given
        line-length and that a newline lies between them.

        :param shortlog_length:            The maximum length of the shortlog.
                                           The shortlog is the first line of
                                           the commit message. The newline
                                           character at end does not count to
                                           the length.
        :param body_line_length:           The maximum line-length of the body.
                                           The newline character at each line
                                           end does not count to the length.
        :param force_body:                 Whether a body shall exist or not.
        :param allow_empty_commit_message: Whether empty commit messages are
                                           allowed or not.
        :param shortlog_regex:             A regex to check the shortlog with.
                                           A full match of this regex is then
                                           required. Passing an empty string
                                           disable the regex-check.
        :param shortlog_trailing_period:   Whether a dot shall be enforced at
                                           the end of the shortlog line.
                                           Providing ``None`` means
                                           "doesn't care".
        """
        with change_directory(self.get_config_dir() or os.getcwd()):
            stdout, stderr = run_shell_command("git log -1 --pretty=%B")

        if stderr:
            self.err("git:", repr(stderr))
            return

        stdout = stdout.rstrip("\n").splitlines()

        if len(stdout) == 0:
            if not allow_empty_commit_message:
                yield Result(self, "HEAD commit has no message.")
            return

        yield from self.check_shortlog(shortlog_length,
                                       shortlog_regex,
                                       shortlog_trailing_period,
                                       stdout[0])
        yield from self.check_body(body_line_length, force_body, stdout[1:])

    def check_shortlog(self,
                       shortlog_length,
                       regex,
                       shortlog_trailing_period,
                       shortlog):
        """
        Checks the given shortlog.

        :param shortlog_length:          The maximum length of the shortlog.
                                         The newline character at end does not
                                         count to the length.
        :param regex:                    A regex to check the shortlog with.
        :param shortlog_trailing_period: Whether a dot shall be enforced at end
                                         end or not (or ``None`` for "don't
                                         care").
        :param shortlog:                 The shortlog message string.
        """
        diff = len(shortlog) - shortlog_length
        if diff > 0:
            yield Result(self,
                         "Shortlog of HEAD commit is {} character(s) longer "
                         "than the limit ({} > {}).".format(
                             diff, len(shortlog), shortlog_length))

        if (shortlog[-1] != ".") == shortlog_trailing_period:
            yield Result(self,
                         "Shortlog of HEAD commit contains no period at end."
                         if shortlog_trailing_period else
                         "Shortlog of HEAD commit contains a period at end.")

        if regex != "":
            match = re.match(regex, shortlog)
            # fullmatch() inside re-module exists sadly since 3.4, but we
            # support 3.3 so we need to check that the regex matched completely
            # ourselves.
            if not match or match.end() != len(shortlog):
                yield Result(
                    self,
                    "Shortlog of HEAD commit does not match given regex.")

    def check_body(self, body_line_length, force_body, body):
        """
        Checks the given commit body.

        :param body_line_length: The maximum line-length of the body. The
                                 newline character at each line end does not
                                 count to the length.
        :param force_body:       Whether a body shall exist or not.
        :param body:             The commit body splitted by lines.
        """
        if len(body) == 0:
            if force_body:
                yield Result(self, "No commit message body at HEAD.")
            return

        if body[0] != "":
            yield Result(self, "No newline between shortlog and body at HEAD.")
            return

        if any(len(line) > body_line_length for line in body[1:]):
            yield Result(self, "Body of HEAD commit contains too long lines.")
