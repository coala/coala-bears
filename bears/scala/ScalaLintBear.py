from os.path import abspath, dirname, join

from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.DistributionRequirement import (
    DistributionRequirement)


scalastyle_config_file = join(dirname(abspath(__file__)),
                              'scalastyle_config.xml')


@linter(executable='java',
        output_format='regex',
        output_regex=r'(?P<severity>warning) file=.+ message=(?P<message>.+) '
                     r'line=(?P<line>\d+)(?: column=(?P<column>\d+))?')
class ScalaLintBear:
    """
    Check Scala code for codestyle, but also semantical problems,
    e.g. cyclomatic complexity.
    """

    LANGUAGES = {'Scala'}
    REQUIREMENTS = {DistributionRequirement(apt_get='default-jre')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    INCLUDE_LOCAL_FILES = {'scalastyle.jar', 'scalalint_config.xml'}
    CAN_DETECT = {'Formatting', 'Complexity'}

    def setup_dependencies(self):
        type(self).jar = self.download_cached_file(
            'https://oss.sonatype.org/content/repositories/releases/org/'
            'scalastyle/scalastyle_2.10/0.8.0/scalastyle_2.10-0.8.0-batch.jar',
            'scalastyle.jar')

    @staticmethod
    def create_arguments(filename, file, config_file,
                         scalalint_config: str=scalastyle_config_file):
        """
        :param scalalint_config: Path to a custom configuration file.
        """
        return ('-jar', ScalaLintBear.jar, filename, '--config',
                scalalint_config)
