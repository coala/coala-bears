from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GoRequirement import GoRequirement
from coalib.results.RESULT_SEVERITY import RESULT_SEVERITY
from coalib.settings.Setting import typed_list


@linter(executable='gometalinter',
        output_format='regex',
        output_regex=r'\w+\.go:'
                     r'(?P<line>\d+):'
                     r'(?P<column>\d*):'
                     r'(?P<severity>[a-z]+): '
                     r'(?P<message>.*) '
                     r'(?P<additional_info>\([a-z]+\))',
        severity_map={'error': RESULT_SEVERITY.MAJOR,
                      'warning': RESULT_SEVERITY.NORMAL})
class GoMetaLintBear:
    """
    Lints your Go files!
    Concurrently runs a number of Go lint tools.
    """

    LANGUAGES = {'Go'}
    REQUIREMENTS = {
        GoRequirement(package='github.com/alecthomas/gometalinter', flag='-u')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    SEE_MORE = 'http://gopkg.in/alecthomas/gometalinter.v2'

    def create_arguments(self, filename, file, config_file,
                         enable_checks: typed_list(str) = (),
                         enable_all_checks: bool = False,
                         disable_checks: typed_list(str) = (),
                         disable_all_checks: bool = False,
                         gometalinter_config_file: str = '',
                         ):
        """
        :param enable_checks:
            List of linters to enable. Some linters are disabled by default.
            Refer https://github.com/alecthomas/gometalinter#supported-linters
        :param enable_all_checks:
            Enable all supported linters.
        :param disable_checks:
            List of linters to disable.
        :param disable_all_checks:
            Disable all supported linters.
        :param gometalinter_config_file:
            A JSON configuration file for gometalinter.
            It overrides ``.gometalinter.json`` which is picked up by
            default, if present. Provide ``False`` in order to prevent this
            default pickup behavior.
        """
        # Arguments are parsed in order.
        args = (filename,)

        if (enable_checks and enable_all_checks) or (
                    disable_checks and disable_all_checks):
            self.err('The arguments you provided are mutually exclusive.')
            return

        if enable_checks and disable_all_checks:
            args += ('--disable-all',)
            args += tuple('--enable={}'.format(e) for e in enable_checks)
        elif disable_all_checks:
            args += ('--disable-all',)
        elif enable_checks:
            args += tuple('--enable={}'.format(e) for e in enable_checks)

        if disable_checks and enable_all_checks:
            args += ('--enable-all',)
            args += tuple('--disable={}'.format(e) for e in disable_checks)
        elif enable_all_checks:
            args += ('--enable-all',)
        elif disable_checks:
            args += tuple('--disable={}'.format(d) for d in disable_checks)

        if gometalinter_config_file == 'False':
            args += ('--no-config',)
        elif gometalinter_config_file:
            args += ('--config={}'.format(gometalinter_config_file),)

        return args
