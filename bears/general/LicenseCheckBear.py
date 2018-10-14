from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


@linter(executable='licensecheck',
        output_format='regex',
        output_regex=r'.*: .*UNKNOWN$',
        result_message='No license found.')
class LicenseCheckBear:
    """
    Attempts to check the given file for a license, by searching the start
    of the file for text belonging to various licenses.

    For Ubuntu/Debian users, the ``licensecheck_lines`` option has to be used
    in accordance with the ``licensecheck_tail`` option.
    """
    LANGUAGES = {'All'}
    REQUIREMENTS = {
        DistributionRequirement(
            apt_get='devscripts',
            dnf='licensecheck',
            portage=None,
            zypper='devscripts',
        ),
    }
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'License'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         licensecheck_lines: int = 60,
                         licensecheck_tail: int = 5000,
                         ):
        """
        :param licensecheck_lines:
            Specify how many lines of the file header should be parsed for
            license information. Set to 0 to parse the whole file (and ignore
            ``licensecheck_tail``).
        :param licensecheck_tail:
            Specify how many bytes to parse at end of file. Set to 0 to disable
            parsing from end of file.
        """
        return ('--lines', str(licensecheck_lines), '--tail',
                str(licensecheck_tail), filename)
