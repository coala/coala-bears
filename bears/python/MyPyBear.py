from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.PipRequirement import PipRequirement


@linter(executable='mypy.bat' if platform.system() == 'Windows' else 'mypy',
        output_format='regex',
        output_regex=r'(?P<filename>[^:]+):((?P<line>\d+):)? '
                     r'(?P<severity>[^:]+): (?P<message>.*)')
class MyPyBear:
    """
    Type-checks your Python files.
    Checks optional static typing using the ``mypy`` tool.

    See <http://mypy.readthedocs.io/en/latest/basics.html> for info on how to
    add static typing.
    """
    LANGUAGES = {"Python", "Python 3", "Python 2"}
    REQUIREMENTS = {PipRequirement('mypy-lang', '0.4.3')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    # This detects typing errors, which is pretty unique -- it doesn't
    # make sense to add a category for it.
    CAN_DETECT = set()

    @staticmethod
    def create_arguments(filename, file, config_file):
        return filename,
