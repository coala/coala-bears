from coalib.bears.GlobalBear import GlobalBear
from coalib.results.Result import Result
from dependency_management.requirements.PipRequirement import PipRequirement
from vulture import Vulture


def _find_unused_code(filenames):
    """
    :param filenames: List of filenames to check.
    :return: Generator of Result objects.
    """
    vulture = Vulture()
    vulture.scavenge(filenames)
    for item in vulture.get_unused_code():
        yield Result.from_values(origin='VultureBear',
                                 message=item.message,
                                 file=item.filename,
                                 line=item.first_lineno,
                                 end_line=item.last_lineno,
                                 confidence=item.confidence)


class VultureBear(GlobalBear):
    LANGUAGES = {'Python', 'Python 3'}
    REQUIREMENTS = {PipRequirement('vulture', '0.25.0')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/82256'
    CAN_DETECT = {'Unused Code'}
    SEE_MORE = 'https://github.com/jendrikseipp/vulture'

    def run(self):
        """
        Check Python code for unused variables and functions using `vulture`.
        """
        filenames = list(self.file_dict.keys())
        return _find_unused_code(filenames)
