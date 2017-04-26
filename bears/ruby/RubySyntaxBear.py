from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.AnyOneOfRequirements import (
    AnyOneOfRequirements)
from dependency_management.requirements.CondaRequirement import (
    CondaRequirement)
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


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
    LANGUAGES = {'Ruby'}
    REQUIREMENTS = {
        AnyOneOfRequirements(
            [DistributionRequirement('ruby'),
             CondaRequirement('ruby', '2.2.3', 'bioconda'),
             ],
        ),
    }
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file):
        return '-wc', filename
