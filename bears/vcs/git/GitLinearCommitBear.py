from bears.vcs.VCSCommitMetadataBear import COMMIT_TYPE
from bears.vcs.git.GitCommitMetadataBear import GitCommitMetadataBear
from coalib.bears.GlobalBear import GlobalBear
from coalib.results.Result import Result


class GitLinearCommitBear(GlobalBear):
    LANGUAGES = {'Git'}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'

    BEAR_DEPS = {GitCommitMetadataBear}

    def run(self, dependency_results,
            git_rebase_help_url: str =
            'http://www.bitsnbites.eu/a-tidy-linear-git-history/',
            **kwargs):
        """
        Inspect the HEAD commit to check if it is a
        git merge commit and return result accordingly.

        :param git_rebase_help_url: web url to get more information
                                    about git rebase
        """
        for result in dependency_results[GitCommitMetadataBear.name]:

            if COMMIT_TYPE.merge_commit in result.commit_type:
                yield Result(self, 'Merge commit is not allowed. '
                                   'Please perform git rebase instead. '
                                   '%s shows how to do rebasing.' % (
                                    git_rebase_help_url))
