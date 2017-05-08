from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GoRequirement import GoRequirement


@linter(executable='gometalinter.v1',
        use_stdout=True,
        output_format='regex',
        output_regex=r'(.*):(?P<line>\d*):(?P<column>\d*):'
                      '(?P<message>.*) \((?:\w*)\)')
class GoMetaLinterBear:
    """
    Checks the ``go`` code using ``gometalinter``. This will run
    some set of golang linters over each file separately.
    """
    LANGUAGES = {'Go'}
    REQUIREMENTS = {GoRequirement(
        package='gopkg.in/alecthomas/gometalinter.v1', flag='-u')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Syntax', 'Missing import',
                  'Unused Code', 'Smell', 'Unreachable Code', 'Security'}
    SEE_MORE = 'https://github.com/alecthomas/gometalinter'

    @staticmethod
    def create_arguments(filename, file, config_file,
                         gometalinter_disable: str='',
                         gometalinter_enable: str='',
                         gometalinter_config: str=''):
        """
        :param gometalinter_disable:
            Disable a linter.
        :param gometalinter_enable:
            Enable a linter.
        :param gometalinter_config:
            Path to a custom configuration file.
        """
        args = ()
        if gometalinter_disable:
            args += ('--disable=' + gometalinter_disable,)
        if gometalinter_enable:
            args += ('--enable=' + gometalinter_enable,)
        if gometalinter_config:
            args += ('--config=' + gometalinter_config,)
        return args
