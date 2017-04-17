import nltk
import re
import shutil
import os
from urllib.parse import urlparse

from coalib.bears.GlobalBear import GlobalBear
from dependency_management.requirements.PipRequirement import PipRequirement
from coala_utils.ContextManagers import change_directory
from coalib.misc.Shell import run_shell_command
from coalib.results.Result import Result
from coalib.settings.FunctionMetadata import FunctionMetadata
from coalib.settings.Setting import typed_list


class GitCommitBear(GlobalBear):
    LANGUAGES = {'Git'}
    REQUIREMENTS = {PipRequirement('nltk', '3.2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/e146c9739ojhr8396wedsvf0d'
    CAN_DETECT = {'Formatting'}
    SUPPORTED_HOST_KEYWORD_REGEX = {
        'github': (r'[Cc]lose[sd]?'
                   r'|[Rr]esolve[sd]?'
                   r'|[Ff]ix(?:e[sd])?'),
        'gitlab': (r'[Cc]los(?:e[sd]?|ing)'
                   r'|[Rr]esolv(?:e[sd]?|ing)'
                   r'|[Ff]ix(?:e[sd]|ing)?')
    }
    CONCATENATION_KEYWORDS = [r',', r'\sand\s']

    _nltk_data_downloaded = False

    def setup_dependencies(self):
        if not self._nltk_data_downloaded and bool(
                self.section.get('shortlog_check_imperative', True)):
            nltk.download([
                'punkt',
                'maxent_treebank_pos_tagger',
                'averaged_perceptron_tagger',
            ])
            type(self)._nltk_data_downloaded = True

    @classmethod
    def check_prerequisites(cls):
        if shutil.which('git') is None:
            return 'git is not installed.'
        else:
            return True

    @classmethod
    def get_shortlog_checks_metadata(cls):
        return FunctionMetadata.from_function(
            cls.check_shortlog,
            omit={'self', 'shortlog'})

    @classmethod
    def get_body_checks_metadata(cls):
        return FunctionMetadata.from_function(
            cls.check_body,
            omit={'self', 'body'})

    @classmethod
    def get_issue_checks_metadata(cls):
        return FunctionMetadata.from_function(
            cls.check_issue_reference,
            omit={'self', 'body'})

    @classmethod
    def get_metadata(cls):
        return FunctionMetadata.merge(
            FunctionMetadata.from_function(
                cls.run,
                omit={'self', 'dependency_results'}),
            cls.get_shortlog_checks_metadata(),
            cls.get_body_checks_metadata(),
            cls.get_issue_checks_metadata())

    @staticmethod
    def get_host_from_remotes():
        """
        Retrieve the first host from the list of git remotes.
        """
        remotes, _ = run_shell_command(
            "git config --get-regex '^remote.*.url$'")

        remotes = [url.split()[-1] for url in remotes.splitlines()]
        if len(remotes) == 0:
            return None

        url = remotes[0]
        if 'git@' in url:
            netloc = re.findall(r'@(\S+):', url)[0]
        else:
            netloc = urlparse(url)[1]
        return netloc.split('.')[0]

    def run(self, allow_empty_commit_message: bool = False, **kwargs):
        """
        Check the current git commit message at HEAD.

        This bear ensures automatically that the shortlog and body do not
        exceed a given line-length and that a newline lies between them.

        :param allow_empty_commit_message: Whether empty commit messages are
                                           allowed or not.
        """
        with change_directory(self.get_config_dir() or os.getcwd()):
            stdout, stderr = run_shell_command('git log -1 --pretty=%B')

        if stderr:
            self.err('git:', repr(stderr))
            return

        stdout = stdout.rstrip('\n')
        pos = stdout.find('\n')
        shortlog = stdout[:pos] if pos != -1 else stdout
        body = stdout[pos+1:] if pos != -1 else ''

        if len(stdout) == 0:
            if not allow_empty_commit_message:
                yield Result(self, 'HEAD commit has no message.')
            return

        yield from self.check_shortlog(
            shortlog,
            **self.get_shortlog_checks_metadata().filter_parameters(kwargs))
        yield from self.check_body(
            body,
            **self.get_body_checks_metadata().filter_parameters(kwargs))
        yield from self.check_issue_reference(
            body,
            **self.get_issue_checks_metadata().filter_parameters(kwargs))

    def check_shortlog(self, shortlog,
                       shortlog_length: int=50,
                       shortlog_regex: str='',
                       shortlog_trailing_period: bool=None,
                       shortlog_imperative_check: bool=True,
                       shortlog_wip_check: bool=True):
        """
        Checks the given shortlog.

        :param shortlog:                 The shortlog message string.
        :param shortlog_length:          The maximum length of the shortlog.
                                         The newline character at end does not
                                         count to the length.
        :param shortlog_regex:           A regex to check the shortlog with.
        :param shortlog_trailing_period: Whether a dot shall be enforced at end
                                         end or not (or ``None`` for "don't
                                         care").
        :param shortlog_wip_check:       Whether a "WIP" in the shortlog text
                                         should yield a result or not.
        """
        diff = len(shortlog) - shortlog_length
        if diff > 0:
            yield Result(self,
                         'Shortlog of the HEAD commit contains {} '
                         'character(s). This is {} character(s) longer than '
                         'the limit ({} > {}).'.format(
                              len(shortlog), diff,
                              len(shortlog), shortlog_length))

        if (shortlog[-1] != '.') == shortlog_trailing_period:
            yield Result(self,
                         'Shortlog of HEAD commit contains no period at end.'
                         if shortlog_trailing_period else
                         'Shortlog of HEAD commit contains a period at end.')

        if shortlog_regex:
            match = re.fullmatch(shortlog_regex, shortlog)
            if not match:
                yield Result(
                    self,
                    'Shortlog of HEAD commit does not match given regex:'
                    ' {regex}'.format(regex=shortlog_regex))

        if shortlog_imperative_check:
            colon_pos = shortlog.find(':')
            shortlog = (shortlog[colon_pos + 1:]
                        if colon_pos != -1
                        else shortlog)
            has_flaws = self.check_imperative(shortlog)
            if has_flaws:
                bad_word = has_flaws[0]
                yield Result(self,
                             "Shortlog of HEAD commit isn't in imperative "
                             "mood! Bad words are '{}'".format(bad_word))
        if shortlog_wip_check:
            if 'wip' in shortlog.lower()[:4]:
                yield Result(
                    self,
                    'This commit seems to be marked as work in progress and '
                    'should not be used in production. Treat carefully.')

    def check_imperative(self, paragraph):
        """
        Check the given sentence/s for Imperatives.

        :param paragraph:
            The input paragraph to be tested.
        :return:
            A list of tuples having 2 elements (invalid word, parts of speech)
            or an empty list if no invalid words are found.
        """
        words = nltk.word_tokenize(nltk.sent_tokenize(paragraph)[0])
        # VBZ : Verb, 3rd person singular present, like 'adds', 'writes'
        #       etc
        # VBD : Verb, Past tense , like 'added', 'wrote' etc
        # VBG : Verb, Present participle, like 'adding', 'writing'
        word, tag = nltk.pos_tag(['I'] + words)[1:2][0]
        if(tag.startswith('VBZ') or
           tag.startswith('VBD') or
           tag.startswith('VBG') or
           word.endswith('ing')):  # Handle special case for VBG
            return (word, tag)
        else:
            return None

    def check_body(self, body,
                   body_line_length: int=72,
                   force_body: bool=False,
                   ignore_length_regex: typed_list(str)=(),
                   body_regex: str=None):
        """
        Checks the given commit body.

        :param body:                The body of the commit message of HEAD.
        :param body_line_length:    The maximum line-length of the body. The
                                    newline character at each line end does not
                                    count to the length.
        :param force_body:          Whether a body shall exist or not.
        :param ignore_length_regex: Lines matching each of the regular
                                    expressions in this list will be ignored.
        :param body_regex:          If provided, checks the presence of regex
                                    in the commit body.
        """
        if len(body) == 0:
            if force_body:
                yield Result(self, 'No commit message body at HEAD.')
            return

        if body[0] != '\n':
            yield Result(self, 'No newline found between shortlog and body at '
                               'HEAD commit. Please add one.')
            return

        if body_regex and not re.fullmatch(body_regex, body.strip()):
            yield Result(self, 'No match found in commit message for the '
                               'regular expression provided: %s' % body_regex)

        body = body.splitlines()
        ignore_regexes = [re.compile(regex) for regex in ignore_length_regex]
        if any((len(line) > body_line_length and
                not any(regex.search(line) for regex in ignore_regexes))
               for line in body[1:]):
            yield Result(self, 'Body of HEAD commit contains too long lines. '
                               'Commit body lines should not exceed {} '
                               'characters.'.format(body_line_length))

    def check_issue_reference(self, body,
                              body_close_issue: bool=False,
                              body_close_issue_full_url: bool=False,
                              body_close_issue_on_last_line: bool=False,
                              body_enforce_issue_reference: bool=False):
        """
        Check for matching issue related references and URLs.

        :param body:
            Body of the commit message of HEAD.
        :param body_close_issue:
            GitHub and GitLab support auto closing issues with
            commit messages. When enabled, this checks for matching keywords
            in the commit body by retrieving host information from git
            configuration. By default, if none of ``body_close_issue_full_url``
            and ``body_close_issue_on_last_line`` are enabled, this checks for
            presence of short references like ``closes #213``.
            Otherwise behaves according to other chosen flags.
            More on keywords follows.
            [GitHub](https://help.github.com/articles/closing-issues-via-commit-messages/)
            [GitLab](https://docs.gitlab.com/ce/user/project/issues/automatic_issue_closing.html)
        :param body_close_issue_full_url:
            Checks the presence of issue close reference with a full URL
            related to some issue. Works along with ``body_close_issue``.
        :param body_close_issue_on_last_line:
            When enabled, checks for issue close reference presence on the
            last line of the commit body. Works along with
            ``body_close_issue``.
        :param body_enforce_issue_reference:
            Whether to enforce presence of issue reference in the body of
            commit message.
        """
        if not body_close_issue:
            return

        host = self.get_host_from_remotes()
        if host not in self.SUPPORTED_HOST_KEYWORD_REGEX:
            return

        if body_close_issue_on_last_line:
            body = body.splitlines()[-1]
            result_message = ('Body of HEAD commit does not contain any {} '
                              'reference in the last line.')
        else:
            result_message = ('Body of HEAD commit does not contain any {} '
                              'reference.')

        if body_close_issue_full_url:
            result_info = 'full issue'
            issue_ref_regex = (
                r'https?://{}\S+/issues/(\S+)'.format(re.escape(host)))
        else:
            result_info = 'issue'
            issue_ref_regex = r'(?:\w+/\w+)?#(\S+)'

        concat_regex = '|'.join(kw for kw in self.CONCATENATION_KEYWORDS)
        compiled_joint_regex = re.compile(
            r'(?:{0})\s+'           # match issue related keywords,
                                    # eg: fix, closes etc.

            r'((?:\S(?!{1}))*\S'    # match links/tags
                                    # eg: fix #123, fix https://github.com

            r'(?:\s*(?:{1})\s*'     # match conjunctions like ',','and'

            r'(?!{0})'              # reject if new keywords appear

            r'(?:\S(?!{1}))*\S)*)'  # match links/tags followed after
                                    # conjunctions if any
            r''.format(
                self.SUPPORTED_HOST_KEYWORD_REGEX[host],
                concat_regex))

        matches = compiled_joint_regex.findall(body)

        if body_enforce_issue_reference and len(matches) == 0:
            yield Result(self, result_message.format(result_info))
            return

        compiled_issue_ref_regex = re.compile(issue_ref_regex)
        compiled_issue_no_regex = re.compile(r'[1-9][0-9]*')
        compiled_concat_regex = re.compile(
            r'\s*(?:{})\s*'.format(concat_regex))

        for match in matches:
            for issue in re.split(compiled_concat_regex, match):
                reference = compiled_issue_ref_regex.fullmatch(issue)
                if not reference:
                    yield Result(self, 'Invalid {} reference: '
                                       '{}'.format(result_info, issue))
                elif not compiled_issue_no_regex.fullmatch(reference.group(1)):
                    yield Result(self, 'Invalid issue number: '
                                       '{}'.format(issue))
