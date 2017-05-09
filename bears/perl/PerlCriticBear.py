from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='perlcritic',
        output_format='regex',
        output_regex=r'(?P<message>.+) at '
                     r'line (?P<line>\d+), '
                     r'column (?P<column>\d+)\. '
                     r'(?P<origin>.+) '
                     r'\(Severity: (?P<severity>\d+)\)',
        severity_map={'1': RESULT_SEVERITY.MAJOR,
                      '2': RESULT_SEVERITY.MAJOR,
                      '3': RESULT_SEVERITY.NORMAL,
                      '4': RESULT_SEVERITY.NORMAL,
                      '5': RESULT_SEVERITY.INFO})
class PerlCriticBear:
    """
    Check the code with perlcritic. This will run perlcritic over
    each of the files seperately.
    """

    LANGUAGES = {'Perl'}
    REQUIREMENTS = {
        DistributionRequirement(
            apt_get='libperl-critic-perl',
            brew=None,
            dnf='perl-Perl-Critic',
            portage='dev-perl/Perl-Critic',
            xbps=None,
            yum='perl-Perl-Critic',
            zypper='perl-Perl-Critic',
        ),
    }
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Formatting', 'Code Simplification'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         perlcritic_profile: str=''):
        """
        :param perlcritic_profile: Location of the perlcriticrc config file.
        """
        args = ('--no-color',)
        if perlcritic_profile:
            args += ('--profile', perlcritic_profile)
        return args + (filename,)
