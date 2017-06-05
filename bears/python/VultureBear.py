from coalib.bears.GlobalBear import GlobalBear
from coalib.results.Result import Result
from dependency_management.requirements.PipRequirement import PipRequirement
from vulture import Vulture


def _find_unused_code(filenames):
    """
    :param filenames: List of filenames to check.
    :return: Generator of Result objects.
    """

    def file_lineno(item):
        return (item.filename.lower(), item.lineno)

    vulture = Vulture()
    vulture.scavenge(filenames)
    for item in sorted(
            vulture.unused_funcs + vulture.unused_imports +
            vulture.unused_props + vulture.unused_vars +
            vulture.unused_attrs, key=file_lineno):
        message = 'Unused {0}: {1}'.format(item.typ, item)
        yield Result.from_values(origin='VultureBear',
                                 message=message,
                                 file=item.filename,
                                 line=item.lineno)


class VultureBear(GlobalBear):
    LANGUAGES = {'Python', 'Python 3'}
    REQUIREMENTS = {PipRequirement('vulture', '0.14.0')}
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
