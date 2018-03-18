from coalib.bears.LocalBear import LocalBear
from dependency_management.requirements.DistributionRequirement import DistributionRequirement
from dependency_management.requirements.PipRequirement import PipRequirement
from coalib.results.Diff import Diff
from coalib.results.Result import Result


class BlackBear(LocalBear):
    LANGUAGES = {'Python', 'Python 2', 'Python 3'}
    REQUIREMENTS = {
        DistributionRequirement('python3', version='3.6'),
        PipRequirement('black', '18.4a4'),
    }
    AUTHORS = {'Bence Nagy'}
    AUTHORS_EMAILS = {'bence@underyx.me'}
    LICENSE = 'AGPL'
    CAN_FIX = {'Formatting'}
    SEE_MORE = 'https://github.com/ambv/black'

    def run(self, filename, file, max_line_length: int=88):
        """
        Blackens code — makes code formatting compliant with black.

        This bear works on Python 3.6+ only.

        :param max_line_length: Maximum number of characters for a line.
        """
        import black  # importing here since only Python 3.6+ has it installed

        options = {'line_length': max_line_length}
        corrected = black.format_str(''.join(file), **options).splitlines(True)

        for diff in Diff.from_string_arrays(file, corrected).split_diff():
            yield Result(
                self,
                "The code is not compliant with black's style.",
                affected_code=(diff.range(filename),),
                diffs={filename: diff},
            )
