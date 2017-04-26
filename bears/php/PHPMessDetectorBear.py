from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import typed_list
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)
from dependency_management.requirements.AnyOneOfRequirements import (
    AnyOneOfRequirements)
from dependency_management.requirements.ComposerRequirement import (
    ComposerRequirement)


@linter(executable='phpmd',
        output_format='regex',
        output_regex=r':(?P<line>\d+)\s*(?P<message>.*)')
class PHPMessDetectorBear:
    """
    The bear takes a given PHP source code base and looks for several
    potential problems within that source. These problems can be things like:

    - Possible bugs
    - Suboptimal code
    - Overcomplicated expressions
    - Unused parameters, methods, properties
    """

    LANGUAGES = {'PHP'}
    REQUIREMENTS = {
        AnyOneOfRequirements(
            [DistributionRequirement(apt_get='phpmd',
                                     dnf='php-phpmd-PHP-PMD',
                                     ),
             ComposerRequirement('phpmd/phpmd'),
             ],
        ),
    }
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Complexity', 'Unused Code', 'Redundancy',
                  'Variable Misuse'}
    SEE_MORE = 'https://phpmd.org/about.html'

    @staticmethod
    def create_arguments(filename, file, config_file,
                         phpmd_rulesets: typed_list(str)):
        """
        :param phpmd_rulesets:
            A list of rulesets to use for analysis.
            Available rulesets: cleancode, codesize, controversial, design,
            naming, unusedcode.
        """
        return filename, 'text', ','.join(phpmd_rulesets)
