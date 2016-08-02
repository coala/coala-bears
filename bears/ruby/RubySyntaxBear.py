from coalib.bearlib.abstractions.Linter import linter
from coalib.bears.requirements.GemRequirement import GemRequirement


@linter(executable='ruby',
        use_stdout=False,
        use_stderr=True,
        output_format='regex',
        output_regex=r'.+?:(?P<line>\d+): (?P<message>.*?'
                     r'(?P<severity>error|warning)[,:] \S+)\s?'
                     r'(?:\S+\s(?P<column>.*?)\^)?')
class RubySyntaxBear:
    """
    Checks the code with ``ruby -wc`` on each file separately.
    """
    LANGUAGES = {"Ruby"}
    REQUIREMENTS = {GemRequirement('ruby', '2.1.5')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '-wc', filename
