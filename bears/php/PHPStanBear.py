from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.ComposerRequirement import (
    ComposerRequirement)


@linter(executable='phpstan',
        output_format='regex',
        output_regex=r'(?P<line>\d+)  (?P<message>.*)')
class PHPStanBear:
    """
    Checks the code with ``phpstan analyze``.
    This can run it on multiple files and folders.
    See <https://github.com/phpstan/phpstan> for more information.
    """
    LANGUAGES = {'PHP'}
    REQUIREMENTS = {ComposerRequirement('phpstan/phpstan')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Syntax', 'Unused Code', 'Variable Misuse',
                  'Undefined Element', 'Missing Import', 'Spelling'}

    @staticmethod
    def create_arguments(filename, file,
                         config_file,
                         phpstan_level: str='0',
                         phpstan_config: str=''):
        """
        :param phpstan_config:
            path to a custom configuration file.
            When using a custom project config file,
            phpstan_level is set to 1
            (as default value 0 does not apply here).
        :param phpstan_level:
            To set rule levels.
            0 is the loosest and 4 is the strictest.
            See <https://github.com/phpstan/phpstan> for more information.
        """
        args = ('analyse',)
        if phpstan_config != '' and phpstan_level != '0':
            args += ('--level='+phpstan_level, '-c ' +
                     phpstan_config, filename,)
        elif phpstan_config:
            phpstan_level = '1'
            args += ('--level='+phpstan_level, '-c ' +
                     phpstan_config, filename,)
        else:
            args += ('--level='+phpstan_level, filename,)
        return args
