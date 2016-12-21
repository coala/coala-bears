from coalib.bearlib.abstractions.Linter import linter
from dependency_management.requirements.GoRequirement import GoRequirement
from coalib.settings.Setting import typed_list


@linter(executable='errcheck',
        output_format='regex',
        output_regex=r'[^:]+:(?P<line>\d+):'
                     r'(?P<column>\d+)\s*(?P<message>.*)',
        result_message='This function call has an unchecked error.')
class GoErrCheckBear:

    """
    Checks the code for all function calls that have unchecked errors.
    GoErrCheckBear runs ``errcheck`` over each file to find such functions.

    For more information on the analysis visit
    <https://github.com/kisielk/errcheck>.
    """
    LANGUAGES = {'Go'}
    REQUIREMENTS = {GoRequirement(
        package='github.com/kisielk/errcheck', flag='-u')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    ASCIINEMA_URL = 'https://asciinema.org/a/46834'
    CAN_DETECT = {'Syntax'}

    @staticmethod
    def create_arguments(filename, file, config_file,
                         ignore: typed_list(str)=[],
                         ignorepkg: typed_list(str)=[],
                         asserts: bool=False,
                         blank: bool=False):
        """
        Bear configuration arguments.

        :param ignore:       Comma-separated list of pairs of the
                             form package:regex. For each package, the regex
                             describes which functions to ignore within that
                             package. The package may be omitted to have the
                             regex apply to all packages.
        :param ignorepkg:    Takes a comma-separated list of package
                             import paths to ignore.
        :param asserts:      Enables checking for ignored type assertion
                             results.
        :param blank:        Enables checking for assignments of errors to
                             the blank identifier.

        """
        args = ()
        if ignore:
            args += ('-ignore', ','.join(part.strip() for part in ignore))
        if ignorepkg:
            args += ('-ignorepkg', ','.join(part.strip()
                                            for part in ignorepkg))
        if blank:
            args += ('-blank',)
        if asserts:
            args += ('-asserts',)
        return args + (filename,)
