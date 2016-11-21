import re

from coalib.bears.LocalBear import LocalBear
from coalib.results.Result import Result


class PinRequirementsBear(LocalBear):

    LICENSE = 'AGPL'
    LANGUAGES = {
        'Python Requirements',
        'Python 2 Requirements',
        'Python 3 Requirements',
    }
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}

    def run(self, filename, file, require_patch: bool=False):
        """
        Checks if requirements are properly pinned. It will always raise an
        issue if the minor version is not given. If you do not wish that, do
        not use this bear.

        :param require_patch: Requires a patch version specified if True.
        """
        for i, line in enumerate(file, start=1):
            match = re.search(r'[=<>]+([0-9.]+)(?:$|\s|#)', line)
            if not match:
                continue

            if require_patch and len(match.group(0).split('.')) < 3:
                yield Result.from_values(
                    self, 'The patch version is missing.', filename, i)
            elif len(match.group(0).split('.')) < 2:
                yield Result.from_values(
                    self, 'The minor version is missing.', filename, i)
