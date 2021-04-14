from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.DistributionRequirement \
    import DistributionRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY


@linter(executable='nginx',
        output_format='regex',
        output_regex=r'\[(?P<severity>.+)\](?P<message>.+)'
                     r':(?P<line>\d+)',
        severity_map={'emerg': RESULT_SEVERITY.MAJOR,
                      'alert': RESULT_SEVERITY.MAJOR,
                      'warn': RESULT_SEVERITY.NORMAL},
        use_stderr=True)
class NginxBear:
    """
    Checks syntax of nginx configuration files using `nginx -tc` command.
    """

    LANGUAGES = {'nginx'}
    REQUIREMENTS = {
        DistributionRequirement(
            apt_get='nginx',
            brew='nginx',
            dnf='nginx',
            portage=None,
            xbps='nginx',
            yum='nginx',
            zypper='nginx',
        ),
    }
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax'}
    SEE_MORE = 'https://nginx.com'

    @staticmethod
    def create_arguments(filename, file, config_file):
        return ('-tc', filename)
