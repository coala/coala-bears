import glob
import re

from bears.vcs.git.GitCommitMetadataBear import GitCommitMetadataBear
from coalib.bears.GlobalBear import GlobalBear
from coalib.results.Result import Result


class CISkipInspectBear(GlobalBear):
    LANGUAGES = {'Git'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    BEAR_DEPS = {GitCommitMetadataBear}

    SKIP_CI_REGEX = r'\[ci skip\]|\[skip ci\]'

    def run(self, dependency_results,
            appveyor_ci: bool = False,
            **kwargs):
        """
        Most CI allow commits to skip CI build by including sequences
        like [skip ci] or [ci skip] anywhere in the commit message.
        AppVeyor CI supports [skip appveyor] in addition to the above
        but only in the commit title.
        This bear checks the HEAD commit to see if it disables CI build
        and return result accordingly. Supported CI include AppVeyor,
        Bitrise, Circle CI, GitLab CI, Scrutinizer, Semaphore,
        Shippable, Travis CI and wercker.

        :param appveyor_ci:         Whether AppVeyor is used by the
                                    project or not.
        """
        if appveyor_ci:
            self.SKIP_CI_REGEX += r'|\[skip appveyor\]'

        for result in dependency_results[GitCommitMetadataBear.name]:

            if appveyor_ci:
                pos = result.raw_commit_message.find('\n')
                commit_title = result.raw_commit_message[:pos] if (
                    pos != -1) else result.raw_commit_message

            else:
                commit_title = result.raw_commit_message

            match = re.search(self.SKIP_CI_REGEX, commit_title)
            if not match:
                continue

            all_files = (result.modified_files +
                         result.added_files + result.deleted_files)

            for file in all_files:
                for pattern in self.section['files']:
                    if file not in glob.glob(pattern):
                        continue
                    yield Result(
                        self,
                        'This commit modifies a file that has '
                        'pattern of type "%s", thus should '
                        'not disable CI build.' %
                        pattern)
