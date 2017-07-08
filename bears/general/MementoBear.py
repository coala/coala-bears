from bears.general.MementoFetchBear import MementoFetchBear

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY

from dependency_management.requirements.PipRequirement import PipRequirement


class MementoBear(LocalBear):
    DEFAULT_TIMEOUT = 15
    LANGUAGES = {'All'}
    REQUIREMENTS = {PipRequirement('memento-client', '0.6.1')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Documentation'}
    BEAR_DEPS = {MementoFetchBear}

    def run(self, filename, file, dependency_results=dict()):
        """
        Find links in any text file and check if they are archived.

        Link is considered valid if the link has been archived by any services
        in memento_client.

        This bear can automatically fix redirects.

        Warning: This bear will make HEAD requests to all URLs mentioned in
        your codebase, which can potentially be destructive. As an example,
        this bear would naively just visit the URL from a line that goes like
        `do_not_ever_open = 'https://api.acme.inc/delete-all-data'` wiping out
        all your data.

        :param dependency_results: Results given by MementoFetchBear.
        """
        for result in dependency_results.get(MementoFetchBear.name, []):
            if result.contents:
                continue

            if result.redirected:
                yield Result(
                    self,
                    ('This link redirects to {url} and not archived yet, '
                     'visit https://web.archive.org/save/{url} to get it '
                     'archived.'.format(url=result.link)
                     ),
                    affected_code=result.affected_code,
                    severity=RESULT_SEVERITY.INFO
                )
            else:
                yield Result(
                    self,
                    ('This link is not archived yet, visit '
                     'https://web.archive.org/save/%s to get it archived.'
                     % result.link),
                    affected_code=result.affected_code,
                    severity=RESULT_SEVERITY.INFO
                )
